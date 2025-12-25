-- 1. Таблица пользователей
CREATE TABLE IF NOT EXISTS public.users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    mail TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL CHECK (role IN ('client', 'support', 'admin')),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- 2. Таблица диалогов (тикетов)
-- Тикет — это сессия чата. У пользователя может быть только один открытый тикет.
CREATE TABLE IF NOT EXISTS public.tickets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITHOUT TIME ZONE,
    
    CONSTRAINT fk_tickets_user 
        FOREIGN KEY (user_id) 
        REFERENCES public.users (id) 
        ON DELETE CASCADE
);

-- ВАЖНО: Уникальный индекс, запрещающий создавать второй открытый тикет
-- Если есть запись с status='open' для этого user_id, база не даст создать вторую.
CREATE UNIQUE INDEX IF NOT EXISTS idx_one_open_ticket_per_user 
    ON public.tickets (user_id) 
    WHERE (status = 'open');

-- 3. Таблица сообщений
CREATE TABLE IF NOT EXISTS public.messages (
    id BIGSERIAL PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    sender_id BIGINT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_messages_ticket 
        FOREIGN KEY (ticket_id) 
        REFERENCES public.tickets (id) 
        ON DELETE CASCADE,

    CONSTRAINT fk_messages_sender 
        FOREIGN KEY (sender_id) 
        REFERENCES public.users (id) 
        ON DELETE SET NULL
);

-- Индекс для быстрой загрузки истории конкретного чата
CREATE INDEX IF NOT EXISTS idx_messages_by_ticket 
    ON public.messages (ticket_id, created_at);
