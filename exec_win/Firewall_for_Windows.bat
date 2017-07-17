set exePath=%~dp0
netsh advfirewall firewall add rule name=AreaD8 dir=in action=allow program=%exePath%\aread8.exe ENABLE=yes
netsh advfirewall firewall add rule name=AreaDinf dir=in action=allow program=%exePath%\areadinf.exe ENABLE=yes
netsh advfirewall firewall add rule name=ConnectDown dir=in action=allow program=%exePath%\connectdown.exe ENABLE=yes
netsh advfirewall firewall add rule name=Curvature dir=in action=allow program=%exePath%\curvature.exe ENABLE=yes
netsh advfirewall firewall add rule name=D8DistDownToStream dir=in action=allow program=%exePath%\d8distdowntostream.exe ENABLE=yes
netsh advfirewall firewall add rule name=D8DistUpToRidge dir=in action=allow program=%exePath%\d8distuptoridge.exe ENABLE=yes
netsh advfirewall firewall add rule name=D8FlowDir dir=in action=allow program=%exePath%\d8flowdir.exe ENABLE=yes
netsh advfirewall firewall add rule name=DinfDistDown dir=in action=allow program=%exePath%\dinfdistdown.exe ENABLE=yes
netsh advfirewall firewall add rule name=DinfDistUpToRidge dir=in action=allow program=%exePath%\dinfdistuptoridge.exe ENABLE=yes
netsh advfirewall firewall add rule name=DinfFlowDir dir=in action=allow program=%exePath%\dinfflowdir.exe ENABLE=yes
netsh advfirewall firewall add rule name=DropAnalysis dir=in action=allow program=%exePath%\dropanalysis.exe ENABLE=yes
netsh advfirewall firewall add rule name=FuzzySlpPosInference dir=in action=allow program=%exePath%\fuzzyslpposinference.exe ENABLE=yes
netsh advfirewall firewall add rule name=HardenSlpPos dir=in action=allow program=%exePath%\hardenslppos.exe ENABLE=yes
netsh advfirewall firewall add rule name=MoveOutletsToStreams dir=in action=allow program=%exePath%\moveoutletstostreams.exe ENABLE=yes
netsh advfirewall firewall add rule name=PitRemove dir=in action=allow program=%exePath%\pitremove.exe ENABLE=yes
netsh advfirewall firewall add rule name=SelectTypLocSlpPos dir=in action=allow program=%exePath%\selecttyplocslppos.exe ENABLE=yes
netsh advfirewall firewall add rule name=SimpleCalculator dir=in action=allow program=%exePath%\simplecalculator.exe ENABLE=yes
netsh advfirewall firewall add rule name=Threshold dir=in action=allow program=%exePath%\threshold.exe ENABLE=yes
::pause
