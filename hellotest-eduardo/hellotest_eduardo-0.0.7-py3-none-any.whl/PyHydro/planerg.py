from PyHydro import mddh
import os

sistema = mddh(os.path.join(os.getcwd(), 'pmo/'))

#i = 161
# sistema.conf_uh[i].PlotaPCV()
# sistema.conf_uh[i].PlotaPCA()
# sistema.conf_uh[i].PlotaProdutibs(0,0)
# sistema.conf_uh[i].PlotaVazoes()
# sistema.conf_uh[i].PlotaColina()
# sistema.conf_uh[i].PlotaVolume()
# sistema.conf_uh[i].PlotaVazMin()
# sistema.conf_uh[i].PlotaVolMorto()
# sistema.conf_uh[i].PlotaPotencia()
# sistema.Plota_Expansao_Uh()

# sistema.PlotaMercado()
# for i, iree in enumerate(sistema.ree):
#     sistema.ree[i].PlotaEArmMax(sistema.conf_uh)
# for i, isist in enumerate(sistema.submercado):
#     sistema.submercado[i].PlotaEArmMax(sistema.conf_uh)
#sistema.PlotaEArmMaxSist()
#sistema.PlotaEArmMaxRee()
# sistema.submercado[1].PlotaMercado()

#for ires in sistema.ree:
#    ires.PlotaEArmMax(sistema.conf_uh)
#for isis in sistema.ree:
#    isis.PlotaENA()

#for isis in sistema.submercado:
#    isis.PlotaENA()

sistema.conf_uh[7].parp(sistema.ordmaxparp)
sistema.conf_uh[7].PlotaParp(3)
sistema.conf_uh[7].gera_series_aditivo()

#for imes in range(12):
#    sistema.conf_uh[7].PlotaParp(imes)
#sistema.conf_uh[i].gera_series_aditivo()
#sistema.conf_uh[7].gera_series_multiplicativo()

#sistema.conf_uh[i].parp_otimo(6)
#sistema.conf_uh[i].pso(11)
#sistema.conf_uh[i].gera_series_multiplicativo_parp_otimo()

#sistema.pde(11, 5, 12)
#sistema.plota_corte(1,11)
#sistema.plota_corte(5,21)


