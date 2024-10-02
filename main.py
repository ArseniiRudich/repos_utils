from pathlib import Path
import json
import pandas as pd

AUTHOR_KEY = 'author'
REPO_KEY = 'repo'

def normalize(df:pd.DataFrame) -> pd.DataFrame:
  return df.drop_duplicates().sort_values(by=[AUTHOR_KEY, REPO_KEY])

def load_repos(path: Path) -> pd.DataFrame:
  with path.open() as file:
    df = pd.DataFrame([json.loads(line) for line in file])
  df_res = normalize(df)
  print(f"loading file ={path} size={df.shape[0]} deduplicated size={df_res.shape[0]}")
  return df_res


def merge(dfs: list[pd.DataFrame]) -> pd.DataFrame:
  return normalize(pd.concat(dfs))

def write_repos(path: Path, df:pd.DataFrame) -> None:
  with path.open('w') as file:
    for _, row in df.iterrows():
      file.write(f'{json.dumps(dict(row))}\n')


if __name__ == '__main__':
  root_path = Path('~/temp/groovy_repos/').expanduser()
  old_repos = load_repos(root_path/'groovy.old.jsonl')
  new_repos = load_repos(root_path/'groovy.new.jsonl')
  repos = merge([new_repos, old_repos])
  print(f'combined repos size={repos.shape[0]}')
  write_repos(root_path/'groovy.repos.jsonl', repos)