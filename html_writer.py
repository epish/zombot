import settings
import vkutils

class AppHtmlWriter():
    def __init__(self, app_id, settings_filename):
        _settings = settings.Settings(settings_filename)
        self.__params = vkutils.VK(_settings).getAppParams(app_id)

    def write(self, filename):
        html = self._getHtml()
        with open(filename, 'w') as f:
            f.write(html)

    def _getHtml(self):
        html = ('''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title>zombiefarm</title>

<body>
<object
                type="application/x-shockwave-flash"
                id="flashobj"
                data="http://s.shadowlands.ru/zombievk-res/zombiefarm.swf?ver=f6fddb4c3ab302562f2e74bb7f4bae702b5f33de"
                width="100%"
                height="100%">
                <param name="width" value="707">
                <param name="height" value="730">
                <param name="allowScriptAccess" value="always">
                <param name="allowFullScreen" value="true">
                <param name="wmode" value="window">
                <param name="flashvars" value="''')
        html += self._getFlashVars()
        html += '''">
                </object></body></html>
'''
        return html

    def _getFlashVars(self):
        items = self.__params
        params = []
        for key, value in items.iteritems():
            params.append(key + "=" + str(value))
        flashVars = "&".join(params)
        return flashVars


if __name__ == '__main__':
    writer = AppHtmlWriter(612925, 'settings.ini')
    writer.write('zombiefarm.html')