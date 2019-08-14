-- таблица разделов форума:
CREATE TABLE forum.public.sections (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE forum.public.sections_search (
    section_id INTEGER NOT NULL PRIMARY KEY,
    title tsvector NOT NULL,
    CONSTRAINT fk_section_id FOREIGN KEY (section_id)
      REFERENCES forum.public.sections(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX sections_search_title
    ON forum.public.sections_search
        USING gin(title);

-- таблица постов в разделах форума:
CREATE TABLE forum.public.posts
(
    id          SERIAL PRIMARY KEY,
    section_id  INTEGER      NOT NULL,
    title       VARCHAR(128) NOT NULL,
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP,
    CONSTRAINT fk_section_id FOREIGN KEY (section_id)
        REFERENCES forum.public.sections (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE forum.public.posts_search (
    post_id INTEGER NOT NULL PRIMARY KEY,
    title tsvector NOT NULL,
    CONSTRAINT fk_posts_id FOREIGN KEY (post_id)
      REFERENCES forum.public.posts(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX posts_search_title
    ON forum.public.posts_search
        USING gin(title);

-- таблица комментариев постов:
CREATE TABLE forum.public.comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    level INTEGER NOT NULL,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_section_id FOREIGN KEY (post_id)
      REFERENCES forum.public.posts(id)
      ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_parent_id FOREIGN KEY (parent_id)
      REFERENCES forum.public.comments(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);
