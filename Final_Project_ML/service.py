import os
import hashlib

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from catboost import CatBoostClassifier
from typing import List


load_dotenv()

# Database =
# postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000
    engine = create_engine(os.getenv('DATABASE'))
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)


def load_features(select) -> pd.DataFrame:
    return batch_load_sql(select)


def get_model_path(path: str) -> str:
    if os.environ.get('IS_LMS') == '1':
        return '/workdir/user_input/model'
    return path


def load_models():
    model_path_control = get_model_path(os.getenv('PATH_CONTROL'))
    model_path_test = get_model_path(os.getenv('PATH_TEST'))
    from_file_control = CatBoostClassifier()
    from_file_control.load_model(model_path_control)
    from_file_test = CatBoostClassifier()
    from_file_test.load_model(model_path_test)
    return from_file_control, from_file_test


def load_model():
    model_test, model_control = load_models()
    print('Models uploaded')
    return model_test, model_control


def load_posts():
    posts = load_features("SELECT * ...")
    posts_text = posts[['post_id', 'text', 'topic']]
    print('Posts uploaded')
    return posts.drop('text', axis=1), posts_text


def load_users():
    users = load_features("SELECT * ...")
    print('Users uploaded')
    return users


model, model_test = load_model()
posts, posts_text = load_posts()
users = load_users()


def predict_posts(user_id: int, limit: int):
    features = pd.merge(users[users['user_id'] == user_id], posts, how='cross')
    features_final_unordered = features.drop(['user_id', 'post_id'], axis=1)
    desired_order = [
        'gender', 'age', 'country', 'city', 'exp_group', 'os', 'source',
        'favorite_topic', 'topic', 'average_sentence_length', 'post_len',
        'tsne-2d-one', 'tsne-2d-two', 'cluster', 'total_likes', 'like_rate',
        'avg_liking_age'
    ]
    features_final = features_final_unordered.reindex(columns=desired_order)
    features['probas'] = model.predict_proba(features_final)[:, 1]
    top_posts = features.sort_values('probas', ascending=False).iloc[:limit]
    return top_posts['post_id'].tolist()


def predict_test_posts(user_id: int, limit: int):
    features = pd.merge(users[users['user_id'] == user_id], posts, how='cross')
    features_final_unordered = features.drop(['user_id', 'post_id'], axis=1)
    desired_order = [
        'gender', 'age', 'country', 'city', 'exp_group', 'os', 'source',
        'favorite_topic', 'topic', 'average_sentence_length', 'post_len',
        'tsne-2d-one', 'tsne-2d-two', 'cluster', 'total_likes', 'like_rate',
        'avg_liking_age'
    ]
    features_final = features_final_unordered.reindex(columns=desired_order)
    features['probas'] = model_test.predict_proba(features_final)[:, 1]
    top_posts = features.sort_values('probas', ascending=False).iloc[:limit]
    return top_posts['post_id'].tolist()


def load_post_texts(post_ids: List[int]) -> List[dict]:
    records = posts_text[posts_text['post_id'].isin(post_ids)]
    return records.to_dict("records")


def get_exp_group(user_id: int) -> str:
    res = int(
        hashlib.md5((str(user_id) + 'my_unique_salt').encode()).hexdigest(), 16
    ) % 2
    return str(res)
