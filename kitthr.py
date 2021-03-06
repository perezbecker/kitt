from btle import Peripheral, ADDR_TYPE_PUBLIC, AssignedNumbers
import time

class HRM(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_PUBLIC)

if __name__=="__main__":
    cccid = AssignedNumbers.client_characteristic_configuration
    hrmid = AssignedNumbers.heart_rate
    hrmmid = AssignedNumbers.heart_rate_measurement

    hrm = None
    
    while True: 

        try:
            hrm = HRM('F4:B8:5E:EB:C2:BA')
        
            service, = [s for s in hrm.getServices() if s.uuid==hrmid]
            ccc, = service.getCharacteristics(forUUID=str(hrmmid))
        
            if 0: # This doesn't work
                ccc.write('\1\0')
        
            else:
                desc = hrm.getDescriptors(service.hndStart,
                                          service.hndEnd)
                d, = [d for d in desc if d.uuid==cccid]
        
                hrm.writeCharacteristic(d.handle, '\1\0')
        
            
            def print_hr(cHandle, data):
                bpm = ord(data[1])
                output = open('/mnt/usb/kittlogs/hr.txt','w')
		print >> output, bpm, int(time.time())
		output.close()
		print bpm
            hrm.delegate.handleNotification = print_hr
        
        
            hrm.waitForNotifications(1.)
        
            if hrm:
                hrm.disconnect()
        
        
        except KeyboardInterrupt:
            hrm.disconnect()
