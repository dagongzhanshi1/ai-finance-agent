-- 创建学习数据库
-- 这个文件可以在 DBeaver 中执行，或者用 sqlite3 命令行运行

-- 股票信息表
CREATE TABLE stocks (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sector TEXT,
    pe_ratio REAL,
    market_cap REAL  -- 市值（亿）
);

-- 插入示例数据
INSERT INTO stocks VALUES
('600519', '贵州茅台', '白酒', 30.5, 25000),
('000858', '五粮液', '白酒', 25.2, 8000),
('300750', '宁德时代', '新能源', 50.1, 15000),
('002594', '比亚迪', '新能源', 35.8, 12000),
('601318', '中国平安', '金融', 12.3, 9000),
('600036', '招商银行', '金融', 8.5, 11000),
('000333', '美的集团', '家电', 15.2, 6000),
('002415', '海康威视', '科技', 22.8, 4500);

-- 查询练习
-- 1. 查询所有股票
SELECT * FROM stocks;

-- 2. 查询市盈率低于 20 的股票
SELECT * FROM stocks WHERE pe_ratio < 20;

-- 3. 按行业分组统计平均市盈率
SELECT sector, AVG(pe_ratio) AS avg_pe, COUNT(*) AS count
FROM stocks
GROUP BY sector
ORDER BY avg_pe;

-- 4. 按市值从高到低排序
SELECT * FROM stocks ORDER BY market_cap DESC;

-- 5. 查询市值超过 10000 亿的白酒股
SELECT * FROM stocks WHERE market_cap > 10000 AND sector = '白酒';
