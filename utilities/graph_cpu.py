from ST7735Control import ST7735Control 
import json
import sys
import os

pad = 5

# TFT is 160 x 128

def graphFrame(mydisplay, start_tuple, height, border = True):
    """
    """
    topLeft = (pad+start_tuple[0], start_tuple[1])
    bottomRight = (160-pad-1, start_tuple[1]+height)
    borderTuple = (topLeft[0], topLeft[1], bottomRight[0], bottomRight[1])
    interiorTuple = (topLeft[0]+1, topLeft[1]+1, bottomRight[0]-1, bottomRight[1]-1)
    ###########################
    # Draw the graph edging/background
    # Gray Box
    mydisplay.drawShape("rectangle", borderTuple, (128,128,128))
    if border:
        # Black Fill
        mydisplay.drawShape("rectangle", interiorTuple, (0,0,0))

def lineGraph(mydisplay, data, scaleMax, graphTuple, justify = "Top", 
              graph_type = "line bezier", color_tuple = (0,0,0)):
    """
    """
    y_offset = graphTuple[1]
    maxHeight = graphTuple[3] - graphTuple[1]
    ###########################
    # Normalize the data
    if justify == "Top":
        data = [(((thisData)*maxHeight/scaleMax)+y_offset) for thisData in data]
    else:
        data = [(((scaleMax-thisData)*maxHeight/scaleMax)+y_offset) for thisData in data]
    ###########################
    # Draw the graph data
    mydisplay.drawShape(graph_type, graphTuple, color_tuple, data)

def graph_data():
    thisFontSize = 12

    # Create a new control object
    mydisplay = ST7735Control(thisTestMode=True, thisFontSize=thisFontSize)
        
    for thisCluster in range(4):
        path = os.path.expanduser("~/data/stats_data_pi4-%d.local.json"%(thisCluster))

        graph_height = 16
        print_y_offset = graph_height*thisCluster + (thisFontSize+3)*thisCluster
        graph_y_offset = graph_height*thisCluster + (thisFontSize+3)*(thisCluster + 1)
        
        # Read in the JSON Data
        with open(path, "r") as json_data:
            data = json.load(json_data)

        # Print info
        mydisplay.printText(( pad, print_y_offset), "Node-%d.local"%(thisCluster), (170,170,170))
        mydisplay.printText(( 105, print_y_offset), "%.1f"%(data["cpu_temp"]), (60,60,170))
        mydisplay.printText(( 140, print_y_offset), "Up", (60,170,60))

        # Draw the Graph Frame
        #graphFrame(mydisplay, (0,graph_y_offset), graph_height)

        # Draw the CPU Utilizatin
        if len(data["cpu_samples"]) > 150-2:
            data_cpu_samples_trimmed = data["cpu_samples"][(len(data["cpu_samples"]) - (150-2)):]
        else:
            data_cpu_samples_trimmed = data["cpu_samples"]
        lineGraph(mydisplay,
            data_cpu_samples_trimmed, 
            100, 
            (5, graph_y_offset, 155, graph_y_offset+graph_height),
            "Bottom",
            "filled bezier",
            (35,115,170)
        )
        
        # Overlay the Memory Utilizatin
        if len(data["mem_samples"]) > 150-2:
            data_mem_samples_trimmed = data["mem_samples"][(len(data["mem_samples"]) - (150-2)):]
        else:
            data_mem_samples_trimmed = data["mem_samples"]
        lineGraph(mydisplay, 
            data_mem_samples_trimmed,
            data["mem_total"],
            (5, graph_y_offset, 155, graph_y_offset+graph_height),
            "Bottom",
            "line bezier",
            (170,45,35)
        )
        
    # Push it to the display...
    mydisplay.update()

if __name__ == "__main__":
    graph_data()
