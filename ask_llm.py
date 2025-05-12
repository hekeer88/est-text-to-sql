import argparse
import os
import json

import openai
from tqdm import tqdm

from models import chatgpt
from models import gemini
from models import deepseek
from utils.enums import LLM
from torch.utils.data import DataLoader

from utils.post_process import process_duplication, get_sqls, remove_gpt4o_characters

QUESTION_FILE = "questions.json"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str)
    parser.add_argument("--openai_api_key", type=str)
    # parser.add_argument("--openai_group_id", type=str, default="org-ktBefi7n9aK7sZjwc2R9G1Wo")
    parser.add_argument("--model", type=str, choices=[
                                                      LLM.GPT_4,
                                                      LLM.GPT_4o,
                                                      LLM.GPT_4o_mini,
                                                      LLM.GPT_o3_mini,
                                                      LLM.Gemini_PRO,
                                                      LLM.Gemini_PRO_1,
                                                      LLM.Gemini_PRO_exp,
                                                      LLM.Gemini_flash,
                                                      LLM.Gemini_flash_light,
                                                      LLM.DeepSeek_reasoner,
                                                      LLM.DeepSeek_chat])
    parser.add_argument("--start_index", type=int, default=0)
    parser.add_argument("--end_index", type=int, default=1000000)
    parser.add_argument("--temperature", type=float, default=1)
    parser.add_argument("--mini_index_path", type=str, default="")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--n", type=int, default=5, help="Size of self-consistent set")
    parser.add_argument("--db_dir", type=str, default="dataset/spider/database")
    args = parser.parse_args()

    questions_json = json.load(open(os.path.join(args.question, QUESTION_FILE), "r"))
    questions = [_["prompt"] for _ in questions_json["questions"]]
    db_ids = [_["db_id"] for _ in questions_json["questions"]]

    if args.model in LLM.OPENAI_MODELS:
        chatgpt.init_chatgpt(args.openai_api_key)
    elif args.model in LLM.GEMINI_MODELS:
        gemini.init_gemini(args.openai_api_key)
    elif args.model in LLM.DEEPSEEK_MODELS:
        deepseek.init_deepseek(args.openai_api_key)
    else:
        raise ValueError(f"Unknown model type for initialization: {args.model}")

    if args.start_index == 0:
        mode = "w"
    else:
        mode = "a"

    if args.mini_index_path:
        mini_index = json.load(open(args.mini_index_path, 'r'))
        questions = [questions[i] for i in mini_index]
        out_file = f"{args.question}/RESULTS_MODEL-{args.model}_MINI.txt"
    else:
        out_file = f"{args.question}/RESULTS_MODEL-{args.model}.txt"

    question_loader = DataLoader(questions, batch_size=args.batch_size, shuffle=False, drop_last=False)

    with open(out_file, mode) as f:
        for i, batch in enumerate(tqdm(question_loader)):
            if i < args.start_index:
                continue
            if i >= args.end_index:
                break
            if args.model in LLM.OPENAI_MODELS:
                try:
                    res = chatgpt.ask_llm(args.model, batch, args.temperature, args.n)
                except openai.error.InvalidRequestError:
                    print(f"The {i}-th question has too much tokens! Return \"SELECT\" instead")
                    res = ""
            if args.model in LLM.DEEPSEEK_MODELS:
                try:
                    res = deepseek.ask_llm(args.model, batch, args.temperature, args.n)
                except openai.error.InvalidRequestError:
                    print(f"The {i}-th question has too much tokens! Return \"SELECT\" instead")
                    res = ""
            elif args.model in LLM.GEMINI_MODELS:
                try:
                    res = gemini.ask_llm(args.model, batch, args.temperature, args.n)
                except Exception as e:
                    print(f"The {i}-th question has too many tokens! Return \"SELECT\" instead")
                    print("Failed question:", batch["question"])
                    print(e)
                    raise e

            if args.n == 1:
                for sql in res["response"]:
                    # remove \n and extra spaces
                    sql = " ".join(sql.replace("\n", " ").split())
                    sql = process_duplication(sql)
                    # python version should >= 3.8
                    if sql.startswith("SELECT"):
                        f.write(sql + "\n")
                    elif sql.startswith(" "):
                        f.write("SELECT" + sql + "\n")
                    else:
                        f.write("SELECT " + sql + "\n")
            else:
                results = []
                cur_db_ids = db_ids[i * args.batch_size: i * args.batch_size + len(batch)]
                for sqls, db_id in zip(res["response"], cur_db_ids):
                    processed_sqls = []
                    for sql in sqls:
                        sql = " ".join(sql.replace("\n", " ").split())
                        sql = process_duplication(sql)
                        sql = remove_gpt4o_characters(sql)
                        if sql.startswith("SELECT"):
                            pass
                        elif sql.startswith(" "):
                            sql = "SELECT" + sql
                        else:
                            sql = "SELECT " + sql
                        processed_sqls.append(sql)
                    result = {
                        'db_id': db_id,
                        'p_sqls': processed_sqls
                    }
                    final_sqls = get_sqls([result], args.n, args.db_dir)

                    for sql in final_sqls:
                        f.write(f"{sql}\t{db_id}\n")
                        # f.write(sql + "\n")
