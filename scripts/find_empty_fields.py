from extras.scripts import *
from dcim.models import *

class FindEmptyFields(Script):
    class Meta:
        name = "Find empty fields"
        description = "Check Empty fields and report them"
        field_order = ['site_name', 'manufacturer']

    site = ObjectVar(
        model=Site,
        required=False
    )
    manufacturer = ObjectVar(
        model=Manufacturer,
        required=False
    )
    
    def tabcalc (self, xdata):
        if (len(xdata)<8): 
            lendata="\t\t\t"
        else:
            if (len(xdata)==8):
                lendata="\t\t"
            else:
                if (len(xdata)<=14):
                    lendata="\t\t"
                else:
                    lendata="\t"
        return lendata

    def run(self, data, commit):
        # number of devices  ---- >>  x = Device.objects.count()
        commit_default = False
        output = "\nid\t|name\t\t\t|ip\t|type\t|serial\t|platform\t|cluster\t|hard\t|ram\t|cpu\t|gpu\t|nic\t|raid\t|ilo\t|iloip\t|ints\t|"
        output = output + "\n--------|-----------------------|-------|-------|-------|---------------|---------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|"
        
        for device in Device.objects.all():
            if (str(device.site) == str(data['site']) or  str(device.device_type.manufacturer.name) == str(data['manufacturer'])):
            
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
                    hardpoint = "-NONE-"
                elif (hardpoint is not 0):
                    hardpoint = "OK"
                
                if (memorypoint == 0):
                    memorypoint = "-NONE-"
                elif (memorypoint is not 0):
                    memorypoint = "OK"

                if (cpupoint == 0):
                    cpupoint = "-NONE-"
                elif (cpupoint is not 0):
                    cpupoint = "OK"

                if (gpupoint == 0):
                    gpupoint = "-NONE-"
                elif (gpupoint is not 0):
                    gpupoint = "OK"

                if (nicpoint <= 1):
                    nicstr = "-NONE-"
                elif (nicpoint > 2):
                    nicstr = "OK"

                if (raidpoint == 0):
                    raidpoint = "-NONE-"
                elif (raidpoint is not 0):
                    raidpoint = "OK"

                inventory = hardpoint + "\t" + "|" + memorypoint + "\t" + "|" + cpupoint + "\t" + "|" + gpupoint + "\t" + "|" + nicstr + "\t" + "|" + raidpoint  + "\t" + "|"

                #INTERFACES SECTION-----------------------------------------------------------------------------------------------------------------------------------------------
                ilopoint = 0
                iloippoint = ""
                intpoint = 0

                # int check
                for iteam in device.interfaces.all():

                    if (str(iteam.name) == "ILO"):
                        ilopoint = ilopoint + 1
                        iloip = "OK"
                    
                    elif "vmk" or "eno" or "vmnic" in str(iteam.name):
                        intpoint = intpoint + 1

                # NONE int check
                if (ilopoint == 0):
                    ilopoint = "-NONE-"
                elif (ilopoint is not 0):
                    ilopoint = "OK"
                
                if (iloippoint == ""):
                    iloippoint = "-NONE-" + "\t"
                elif (iloippoint is not ""):
                    iloippoint = "OK" + "\t"

                if (intpoint == 0):
                    intpoint = "-NONE-"
                elif (intpoint is not 0):
                    intpoint = "OK"
                
                interfaces = ilopoint + "\t" + "|" + iloippoint + "|" + intpoint + "\t" + "|"

                #GENERAL SECTION-----------------------------------------------------------------------------------------------------------------------------------------------

                #if ip is None or empty
                if (str(device.primary_ip4) == "None" or str(device.primary_ip4) == ""):
                    ipv4 = "-NONE-"
                elif (str(device.primary_ip4) != "None" or str(device.primary_ip4) != ""):
                    ipv4 = "OK"

                #if type is None or empty
                if (str(device.device_type) == "None" or str(device.device_type) == ""):
                    devtype = "-NONE-"
                elif (str(device.device_type) != "None" or str(device.device_type) != ""):
                    devtype = "OK"

                #if serial is None or empty
                if (str(device.serial) == "None" or str(device.serial) == ""):
                    serial = "-NONE-"
                elif (str(device.serial) != "None" or str(device.serial) != ""):
                    serial = "OK"

                #if platform is None or empty
                if (str(device.platform) == "None" or str(device.platform) == ""):
                    platform = "-NONE-"
                elif (str(device.platform) != "None" or str(device.platform) != ""):
                    platform = "OK"

                #if cluster is None or empty
                if (str(device.cluster) == "None" or str(device.cluster) == ""):
                    cluster = "-NONE-"
                elif(str(device.cluster) != "None" or str(device.cluster) != ""):
                    cluster = "OK"

                #if RAM is None or empty
                if (str(device.cluster) == "None" or str(device.cluster) == ""):
                    cluster = "-NONE-"
                elif (str(device.cluster) != "None" or str(device.cluster) != ""):
                    cluster = "OK"
                
                nametab = self.tabcalc (device.name)

                output = output + "\n" + str(device.id) + "\t|" + str(device.name) + nametab + "|"  +  ipv4 + "\t|" + devtype + "\t|" + serial + "\t|" + platform + "\t\t|" + cluster + "\t\t|" + inventory + interfaces

            else:
                self.log_failure("XP")
        return(output)
