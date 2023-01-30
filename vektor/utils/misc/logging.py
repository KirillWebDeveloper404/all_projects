import logging
import os

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # filename=f'{os.getcwd()}/logs.log'
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
