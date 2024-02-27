# import contextlib
# import os
# from queue import Queue

# import redis
# import urllib3
# from selenium import webdriver
# from threading import Lock
# import undetected_chromedriver as uc
# from selenium.common import WebDriverException
# import logging

# from terra.constants import TimePeriod
# from terra.utils import Autowired, Injected

# _LOGGER = logging.getLogger(__name__)


# class RestartingWebDriver(uc.Chrome):
#     def __init__(self, *args, **kwargs):
#         self.init_args = args
#         self.init_kwargs = kwargs
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless")
#         super().__init__(*args, **kwargs)
#         self.times_used = 0

#     def is_driver_alive(self):
#         # Method to check if the driver is still responsive
#         try:
#             # Attempt a simple command to check driver's responsiveness
#             self.current_url
#             return True
#         except (WebDriverException, urllib3.exceptions.MaxRetryError):
#             return False

#     def restart_driver(self):
#         self.quit()
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless")
#         super(RestartingWebDriver, self).__init__(*self.init_args, **self.init_kwargs)

#     def ensure_driver_alive_and_reset(self):
#         """
#         Ensure that the driver is alive & reinitialize if necessary. This is necessary because the driver can die.
#         Additionally, kills chrome processes every 10 times it's used to prevent memory leaks.

#         Returns:
#             bool: True if the driver was alive, False otherwise
#         """
#         if not self.is_driver_alive():
#             self.restart_driver()
#             return False
#         return True


# class WebDriverPool:
#     # The env variable is here so we don't get spammed locally when running code, and only run it when necessary
#     # (e.g. on production, or when testing this feature locally)

#     def __init__(self, pool_size=int(os.getenv("WEBDRIVER_POOL_SIZE", 0))):
#         self.pool = Queue(maxsize=pool_size)
#         for _ in range(pool_size):
#             self.pool.put(self.create_driver())

#     def create_driver(self):
#         # Initialize a new WebDriver instance here (e.g., Chrome, Firefox)
#         # the dockerfile we use only supports chrome 108, so we need to use that version
#         return RestartingWebDriver(version_main=int(os.getenv("CHROME_VERSION", 108)), use_subprocess=True)

#     @contextlib.contextmanager
#     @Autowired
#     def get_driver(self, r: redis.Redis = Injected(redis.Redis)):
#         instance_id = os.getenv("INSTANCE_ID", "local")
#         driver = self.pool.get(block=True, timeout=30)
#         if not driver.ensure_driver_alive_and_reset():
#             _LOGGER.info(
#                 "Driver on instance %s was not alive, restarting",
#                 instance_id,
#             )
#         try:
#             yield driver
#         finally:
#             self.release_driver(driver)

#     def release_driver(self, driver: uc.Chrome):
#         if self.is_driver_alive(driver):
#             # Reset the state of the driver before putting it back in the pool
#             driver.delete_all_cookies()
#             self.pool.put(driver)
#         else:
#             # Driver is not responsive, replace it with a new one
#             driver.quit()
#             driver = None
#             self.pool.put(self.create_driver())

#     def close_all_drivers(self):
#         while not self.pool.empty():
#             driver = self.pool.get()
#             driver.quit()
#             driver = None

#     def is_driver_alive(self, driver):
#         # Method to check if the driver is still responsive
#         try:
#             # Attempt a simple command to check driver's responsiveness
#             driver.current_url
#             return True
#         except (WebDriverException, urllib3.exceptions.MaxRetryError):
#             return False
