from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from visual_api import serializers
import subprocess
import time
import boltspy as bolts
import os
repo = bolts.repo
#id невалидных деталей
error_details = ['GenericCircularHollowProfile', 'GenericRectangularHollow', 'GenericSquareHollowProfile', 'OpenbuildsDualVWheel_Delrin', 'OpenbuildsSolidMiniVWheel_Delrin', 'OpenbuildsSolidVWheel_Delrin', 'TSlotExtrusion20x20', 'TSlotExtrusionOneSlot20x20', 'TSlotExtrusionThreeSlots20x20', 'TSlotExtrusionTwoSlots20x20', 'TSlotExtrusionTwoSlotsopp20x20', 'genericPipe', 'tubeBarCrimpedEnds']


class MyViews(APIView):
    

    def get(self, request, format=None):
        details_list = []
        parametrs = {}
        for name in repo.iternames():
            if name[0].name.safe in error_details:
                continue
            parametrs['name'] = name[0].name.nice
            parametrs['id'] = name[0].name.safe
            cl = repo.class_names.get_src(repo.names[name[0].name.safe])
            parametrs['params'] = cl.parameters.tables[0].columns
            new = parametrs.copy()
            details_list.append(new)
            
            
        return Response(details_list)

    def post(self, request):
        #serializer = serializers.VisualSerializer(data=request.data)
        data=request.data
        if data:
            key_det = None
            key_name = None
            values = data.copy()
            list_of_dict_values = list(values.values())
            list_of_dict_values.pop(0)
            res = [eval(i) for i in list_of_dict_values]
            cl = repo.class_names.get_src(repo.names[data['id']])
            for key, value in cl.parameters.tables[0].data.items():
                if res == value:
                    key_det = key
            if key_det:
                key_name = list(cl.parameters.defaults.keys())[0]

                subprocess.call(['freecadcmd', '/home/vadim/diplom2024/my_dip/visual/visual_api/work.py', cl.id, key_name, key_det])
           
                

                return Response(status=status.HTTP_200_OK)

                
            else:
                return Response({"status": "bad_params"}, status=status.HTTP_400_BAD_REQUEST)
                  

        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        

class MyDetail(APIView):
    def get(self, request):
        
        make = request.GET.get("make")
        if make:
            try:
            # create the file response object
                response = StreamingHttpResponse(open('/home/vadim/diplom2024/my_dip/visual/media/detail.stl', 'rb'), content_type='application/vnd.ms-pki.stl')
                
            # set the filename for the response
                response['Content-Disposition'] = 'attachment; filename="detail.stl"'

                os.remove("/home/vadim/diplom2024/my_dip/visual/media/detail.stl")

                return response
                
            except FileNotFoundError:
                raise Http404("File not found")


        else:

            try:
                # create the file response object
                response = StreamingHttpResponse(open('/home/vadim/diplom2024/my_dip/visual/media/detail.stl', 'rb'), content_type='application/vnd.ms-pki.stl')
                    
                # set the filename for the response
                response['Content-Disposition'] = 'attachment; filename="detail.stl"'

                #os.remove("/home/vadim/diplom2024/my_dip/visual/media/detail.stl")

                return response
                    
            except FileNotFoundError:
                raise Http404("File not found")
