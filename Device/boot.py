#esp.osdebug(None)
import webrepl
import network
import gc
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('NNB', 'hgF4RhSeeE')
webrepl.start()
gc.collect()