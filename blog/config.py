class BaseConfig:
    """ 配置基类 """
    SECRET_KEY='harveyblog'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JOBINDEX_PER_PAGE = 9
    COMPNAY_PER_PAGE = 12

class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/blog?charset=utf8"

class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    pass

class TestingConfig(BaseConfig):
    """ 测试环境配置 """
    pass

configs = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
}
    
