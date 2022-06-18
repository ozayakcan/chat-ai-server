from config.ai import AIConfig

class HandleStrings:

  def replaceStrings(data = [], response = ""):
    if "{name}" in response:
      response = response.replace("{name}", HandleStrings.get_data(data, "name", AIConfig.ai_name))
    return response
    
  def get_data(data, arg, defaultValue):
    str = data[arg]
    if str is None:
      return defaultValue
    else:
      return str