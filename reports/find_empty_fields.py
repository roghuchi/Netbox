from dcim.choices import *
from dcim.models import *
from extras.reports import *

class FindEmptyFields(Report):
    class Meta:
        name = "Find empty fields"
        description = "Check Empty fields per device and report them"

    def test_find(self):
        for device in Device.objects.all():
            success_point = 0
            success_str = ""
            failure_point = 0
            failure_str = ""

            #GENERAL SECTION-----------------------------------------------------------------------------------------------------------------------------------------------
            #if ip is None or empty
            if (str(device.primary_ip4) == "None" or str(device.primary_ip4) == ""):
                failure_point = failure_point + 1
                failure_str = failure_str + " IPv4 " + "|"
            elif (str(device.primary_ip4) != "None" or str(device.primary_ip4) != ""):
                success_point = success_point + 1

            #if type is None or empty
            if (str(device.device_type) == "None" or str(device.device_type) == ""):
                failure_point = failure_point + 1
                failure_str = failure_str + " Type " + "|"
            elif (str(device.device_type) != "None" or str(device.device_type) != ""):
                success_point = success_point + 1

            #if serial is None or empty
            if (str(device.serial) == "None" or str(device.serial) == ""):
                failure_point = failure_point + 1
                failure_str = failure_str + " Serial " + "|"
            elif (str(device.serial) != "None" or str(device.serial) != ""):
                success_point = success_point + 1

            #if platform is None or empty
            if (str(device.platform) == "None" or str(device.platform) == ""):
                failure_point = failure_point + 1
                failure_str = failure_str + " Platform " + "|"
            elif (str(device.platform) != "None" or str(device.platform) != ""):
                success_point = success_point + 1

            #if cluster is None or empty
            if (str(device.cluster) == "None" or str(device.cluster) == ""):
                failure_point = failure_point + 1
                failure_str = failure_str + " Cluster " + "|"
            elif(str(device.cluster) != "None" or str(device.cluster) != ""):
                success_point = success_point + 1

            #INTERFACES SECTION-----------------------------------------------------------------------------------------------------------------------------------------------
            ilopoint = 0
            iloippoint = ""
            intpoint = 0

            # int check
            for iteam in device.interfaces.all():

                if (str(iteam.name) == "ILO"):
                    ilopoint = ilopoint + 1
                
                elif "vmk" or "eno" or "vmnic" in str(iteam.name):
                    intpoint = intpoint + 1

            # NONE int check
            if (ilopoint == 0):
                failure_point = failure_point + 1
                failure_str = failure_str + " Ilo " + "|"
            elif (ilopoint is not 0):
                success_point = success_point + 1
            
            if (iloippoint == ""):
                failure_point = failure_point + 1
                failure_str = failure_str + " IloIp " + "|"
            elif (iloippoint is not ""):
                success_point = success_point + 1

            if (intpoint < 2):
                failure_point = failure_point + 1
                failure_str = failure_str + " Ints " + "|"
            elif (intpoint >= 2):
                success_point = success_point + 1

            #INVENTORY SECTION-----------------------------------------------------------------------------------------------------------------------------------------------
            lenip=""
            leniloip=""
            hardpoint = 0
            memorypoint = 0
            cpupoint = 0
            gpupoint = 0
            nicpoint = 0
            raidpoint = 0

            # inventory check
            for iteam in device.inventoryitems.all():

                if (str(iteam.name) == "Hard" or str(iteam.name) == "SSD"):
                    hardpoint = hardpoint + 1
                
                elif (str(iteam.name) == "Memory"):
                    memorypoint = memorypoint + 1

                elif (str(iteam.name) == "CPU"):
                    cpupoint = cpupoint + 1

                elif (str(iteam.name) == "GPU"):
                    cpupoint = cpupoint + 1

                elif (str(iteam.name) == "NIC"):
                    nicpoint = nicpoint + 1
                
                elif (str(iteam.name) == "RAID Card"):
                    raidpoint = raidpoint + 1

            # NONE inventory check
            if (hardpoint == 0):
                failure_point = failure_point + 1
                failure_str = failure_str + " Hard " + "|"
            elif (hardpoint is not 0):
                success_point = success_point + 1
            
            if (memorypoint == 0):
                failure_point = failure_point + 1
                failure_str = failure_str + " Mem " + "|"
            elif (memorypoint is not 0):
                success_point = success_point + 1

            if (cpupoint == 0):
                failure_point = failure_point + 1
                failure_str = failure_str + " CPU " + "|"
            elif (cpupoint is not 0):
                success_point = success_point + 1

            if (gpupoint == 0):
                failure_point = failure_point + 1
                failure_str = failure_str + " GPU " + "|"
            elif (gpupoint is not 0):
                success_point = success_point + 1

            if (nicpoint <= 1):
                failure_point = failure_point + 1
                failure_str = failure_str + " NIC " + "|"
            elif (nicpoint > 2):
                success_point = success_point + 1

            if (raidpoint == 0):
                failure_point = failure_point + 1
                failure_str = failure_str + " Raid " + "|"
            elif (raidpoint is not 0):
                success_point = success_point + 1
            
            if (success_point >= 14):
                self.log_success(device.name,"OK")
            else:
                failure_point = 14 - failure_point
                self.log_failure(str(device.site) + " / " + str(device.name), failure_str + " not exist /////// " + str(failure_point) +" iteam exist")

