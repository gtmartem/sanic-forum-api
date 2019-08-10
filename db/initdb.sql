
-- таблица разделов форума:
CREATE TABLE sections (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- таблица постов в разделах форума:
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_section_id FOREIGN KEY (section_id)
      REFERENCES sections(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);

-- таблица комментариев постов:
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_section_id FOREIGN KEY (post_id)
      REFERENCES posts(id)
      ON UPDATE CASCADE ON DELETE CASCADE
);