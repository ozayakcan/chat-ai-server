from config.ai import AIConfig

class HandleStrings:

  def replaceStrings(data = [], response = ""):
    if "{aiName}" in response:
      response = response.replace("{aiName}", HandleStrings.get_data(data, "aiName", AIConfig.app_name))
    return response
    
  def get_data(data, arg, defaultValue):
    str = data[arg]
    if str is None:
      return defaultValue
    else:
      return str