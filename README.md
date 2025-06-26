## My Gophertalk Backend FastAPI

### Description
This is my simple-stupid project to train FastAPI and SQL... and to torment my [teacher](https://github.com/shekshuev).

### Requirements installing
```bash
pip install fastapi psycopg psycopg-binary psycopg_pool python-dotenv pydantic "python-jose[cryptography]" bcrypt httpx pytest "uvicorn[standard]" regex
```

### Database creating
```sql
CREATE TABLE users (
    id bigserial,
    user_name VARCHAR(30),
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    password_hash VARCHAR(72),
    status SMALLINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT users_id_pkey PRIMARY KEY (id),
    CONSTRAINT users_status_check CHECK (status IN (0, 1))
);

CREATE UNIQUE INDEX users_user_name_uidx 
    ON users (user_name)
    WHERE deleted_at IS NULL;

CREATE TABLE posts (
    id bigserial,
    text VARCHAR(280),
    reply_to_id bigint,
    user_id bigint,
    created_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP,
    CONSTRAINT posts_id_pkey PRIMARY KEY (id),
    CONSTRAINT posts_reply_to_id_fkey FOREIGN KEY (reply_to_id) REFERENCES posts (id),
    CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE views (
    user_id bigint,
    post_id bigint,
    created_at TIMESTAMP DEFAULT now(),
    CONSTRAINT views_user_id_post_id_pkey PRIMARY KEY (user_id, post_id),
    CONSTRAINT views_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT views_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts (id)
);

CREATE TABLE likes (
    user_id bigint,
    post_id bigint,
    created_at TIMESTAMP DEFAULT now(),
    CONSTRAINT likes_user_id_post_id_pkey PRIMARY KEY (user_id, post_id),
    CONSTRAINT likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT likes_post_id_fkey FOREIGN KEY (post_id) REFERENCES posts (id)
);
```