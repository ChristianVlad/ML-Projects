from connection import df_network
from pyvis.network import Network

def process_network_data():
    type_to_color_node = {
        'Comercio': '#FC4B08',
        'Persona': '#091264'
    }

    # Define a mapping of statuses to colors
    status_to_color = {
        'Frozen&Locked': '#091264',
        'Active': '#009a34',
        'Frozen': '#39ABDC',
        'Locked': '#FFB500'
    }

    # Add a new column 'Node_Color_Sources' based on 'sources_type'
    df_network['Node_Color_Sources'] = df_network['sources_type'].map(type_to_color_node)
    df_network['Node_Color_Target'] = df_network['target_type'].map(type_to_color_node)
    df_network['Outline_Node_Color_Sources'] = df_network['sources_status'].map(status_to_color)
    df_network['Outline_Node_Color_Target'] = df_network['target_status'].map(status_to_color)

    # Creating the network with physics disabled
    net = Network(notebook=True, cdn_resources='remote', bgcolor='#ffffff',
                  font_color='black', height='1200px', width='100%', select_menu=True, directed=True)

    # Disable physics
    # net.toggle_physics(False)
    # net.repulsion()

    # Add nodes and edges
    for index, row in df_network.iterrows():
        src = row['sources']
        dts = row['targets']
        src_color = row['Node_Color_Sources']
        dts_color = row['Node_Color_Target']
        src_outline_color = row['Outline_Node_Color_Sources']
        dts_outline_color = row['Outline_Node_Color_Target']
        sources_level = row['sources_level']
        target_level = row['target_level']
        total = row['total']  # Additional attribute from the dataframe

        # Add source node with its corresponding background color and border color
        net.add_node(src, label=src, title=f'VL: {sources_level} Notional amount USD $: {total}',
                     borderWidth=2, color=src_color, borderColor=src_outline_color, inherit_edge_colors=False)

        # Add target node with its corresponding background color and border color
        net.add_node(dts, label=dts, title=f'VL: {target_level} Notional amount USD $:{total}',
                     borderWidth=2, color=dts_color, borderColor=dts_outline_color, inherit_edge_colors=False)

        # Add edge
        net.add_edge(src, dts, color=dts_outline_color)

    return net


def generate_legend_html():
    # Generate HTML for the legend
    legend_html = """
    <div style="position:absolute; top:100px; left:20px; background-color:white; padding:10px; border:1px solid #ddd; border-radius:5px;">
        <p style="margin:0;">Leyenda (Cuentas)</p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#ffffff;"></span></p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#091264;"></span> Persona</p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#FC4B08;"></span>  Comercio </p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#ffffff;"></span></p>
        <p style="margin:0;">Direccionalidad (flechas)</p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#ffffff;"></span></p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#009a34;"></span> Active</p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#091264;"></span> Frozen </p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#FFB500;"></span> Locked </p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#39ABDC;"></span> Frozen&Locked </p>
        <p style="margin:0;"><span style="display:inline-block; width:20px; height:20px; background-color:#ffffff;"></span></p>
    </div>
    """
    return legend_html

def combine_content(index_content, legend_html):
    # Insert legend_html content into index_content at the appropriate location
    legend_insert_position = index_content.find("</body>")
    if legend_insert_position != -1:
        combined_content = index_content[:legend_insert_position] + legend_html + index_content[legend_insert_position:]
    else:
        combined_content = index_content + legend_html

    return combined_content