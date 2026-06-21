"""
Tool Schema — 给 LLM 看的函数说明书
每个工具对应一个 schema，描述它的名字、作用、参数
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "查询 A 股实时股价，输入股票代码（如 600519.SS 表示上交所茅台）",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码，A股需加后缀：.SS=上交所，.SZ=深交所"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pe_ratio",
            "description": "查询股票市盈率(PE)，输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_info",
            "description": "查询公司基本信息（行业、市值），输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_change",
            "description": "查询股票今日涨跌幅百分比，输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_volume",
            "description": "查询股票今日成交量（股数），输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_52week_range",
            "description": "查询股票52周（一年）内的最高价和最低价，输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_financial_metrics",
            "description": "查询公司的财务指标：营收、净利润、毛利率，输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_news",
            "description": "查询股票最新相关新闻（最多5条），输入股票代码",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
]
