import universal_functions as uf
import os
import json
import copy


def main():
    print("Enter the symbol you want to fix")
    path = r"C:\Users\zacha\Documents\main.675.com.ea.game.pvz2_aub.obb.bundle\packet\_PACKAGE_DUMP\DelayLoad_Background_FrontLawn_War.package\resource\images\initial\backgrounds\war_background_effects\library\label\main.xml"
    symbol = uf.open_xml_file(path)

    new_layer_list = []
    layer_list = symbol["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"]
    layer_list = uf.fix_layer_or_frame_list(layer_list, to_layer=True)

    for layer in layer_list:
        frame_list = layer["frames"]["DOMFrame"]
        frame_list = uf.fix_layer_or_frame_list(frame_list, to_layer=True)


        organized_frame_list = dict()
        for frame in frame_list:
            frame_index = int(frame["@index"])

            elements = frame.get("elements", False)
            if not elements: continue
            organized_frame_list[frame_index] = list()

            if elements:
                elements = uf.fix_layer_or_frame_list(elements["DOMSymbolInstance"], to_layer=True)

                for element in elements:
                    to_add_frame = copy.deepcopy(frame)
                    to_add_frame["elements"]["DOMSymbolInstance"] = element
                    organized_frame_list[frame_index].append(to_add_frame)
        
        layers_to_add = dict()
        for frames in organized_frame_list.values():
            for i in range(0, len(frames)):
                if i not in layers_to_add: layers_to_add[i] = []
                layers_to_add[i].append(frames[i])
        
        
        for frame_id in layers_to_add:
            frames = layers_to_add[frame_id]
            first_frame = frames[0]
            if int(first_frame["@index"]) > 0:
                empty_frame = {
                        "@index": "0",
                        "@duration": first_frame["@index"],
                        "@keyMode": "9728",
                        "elements": None
                }
                frames.insert(0, empty_frame)
            
            i = 0
            while i < len(frames)-1:
                
                frame1 = frames[i]
                frame2 = frames[i+1]

                index1 = int(frame1["@index"])
                index2 = int(frame2["@index"])
                duration1 = int(frame1.get("@duration", 1))

                if (index1 + duration1 < index2):
                    empty_frame = {
                        "@index": str(index1+duration1),
                        "@duration": str(index2-index1-1),
                        "@keyMode": "9728",
                        "elements": None
                    }
                    frames.insert(i+1, empty_frame)
                    i += 1
                i += 1

            to_add_layer = copy.deepcopy(layer)
            to_add_layer["frames"]["DOMFrame"] = frames
            to_add_layer["@isSelected"] = False
            new_layer_list.append(to_add_layer)

    symbol["DOMSymbolItem"]["timeline"]["DOMTimeline"]["layers"]["DOMLayer"] = new_layer_list
    uf.write_to_file(symbol, path, is_xml=True)
    print("finished")

            
            


def fix_elements(elements, layer, frame):
    symbol_instances = elements.get("DOMSymbolInstance", False)
    if symbol_instances and isinstance(symbol_instances, dict):
        return frame
    
    frame_list = []


if __name__ == "__main__":
    main()