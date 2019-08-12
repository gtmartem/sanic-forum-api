-- таблица разделов форума:
CREATE TABLE forum.public.sections (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- CREATE TABLE forum.public.sections_title_search (
--     section_id INTEGER NOT NULL,
--     tsvector_title tsvector NOT NULL,
--     CONSTRAINT fk_section_id FOREIGN KEY (section_id)
--       REFERENCES forum.public.sections(id)
--       ON UPDATE CASCADE ON DELETE CASCADE
-- );

-- CREATE INDEX search_tsvector_title
--     ON forum.public.sections_title_search
--         USING gin(tsvector_title);

-- CREATE INDEX search_sections_id
--     ON forum.public.sections_title_search
--         USING btree(section_id);

CREATE INDEX section_id
    ON forum.public.sections
        USING btree(id);

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

CREATE INDEX post_id
    ON forum.public.posts
        USING btree(id);

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

CREATE INDEX comment_id
    ON forum.public.comments
        USING btree(id);