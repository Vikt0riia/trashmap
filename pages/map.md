---
permalink: /map/
homepage: true
---

<div class="paragraph">  
<a href="https://datacatalog.worldbank.org/dataset/what-waste-global-database" style = "position: absolute; ; bottom: 30pt; right: 30pt; z-index: 1;">Data are publically available in World Bank: "What A Waste Global Database"</a>
</div>  

<body>
<!--<div id="container1" style="border:1px dotted blue; width: 700px; height: 475px; position: relative;"></div>-->
<!--<div id="container1" style="  position: fixed; top: 0%; left: 0; bottom: 0; right: 0; overflow: auto;"></div>-->
<div id="container1" style="  position: fixed; top: 0%; left: 0px; bottom: 0; right: 0px; overflow: auto;"></div>
<!--<script src="https://d3js.org/d3.v5.js"></script>-->
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js"></script> 
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3-legend/1.10.0/d3-legend.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script>
<script src="https://datamaps.github.io/scripts/0.4.4/datamaps.world.min.js"></script>


<script src="https://d3js.org/d3-scale.v3.min.js"></script>
<!--<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>-->
<script src="https://d3js.org/d3-axis.v1.min.js"></script>
<script src="https://d3js.org/d3-selection-multi.v1.min.js"></script>

<!--    <script src="https://d3js.org/d3.v4.min.js"></script>-->
<!--<script src="https://d3js.org/d3.v4.min.js"></script>-->   
    

<script>

var dataset = {};
var colorLegend = {};
d3.csv("../country_level_data_0.csv", function(error, csvdata1) {
//
//    // We need to colorize every country based on "numberOfWhatever"
//    // colors should be uniq for every value.
//    // For this purpose we create palette(using min/max series-value)
    var onlyValues = csvdata1.map(function(d){ return d.total_msw_total_msw_generated_tons_year; });
    var minValue = Math.min.apply(null, onlyValues),
            maxValue = Math.max.apply(null, onlyValues);
    

    
    // create color palette function
    var lowColor = "#EFEFFF";
    var highColor = "#02386F"
    var paletteScale = d3.scale.linear()
            .domain([minValue,maxValue])
            .range([lowColor,highColor]); // blue color

//    var paletteScale = d3.scaleSequential()
//        .domain([minValue,maxValue])
//        .interpolator(d3.interpolateViridis);
    
    colorLegend = d3.legend.color()
        .labelFormat(d3.format(".3s"))
        .scale(paletteScale)
        .shapePadding(5)
        .shapeWidth(50)
        .shapeHeight(20)
        .labelOffset(12);
    
    var svg = d3.select("svg");
    
    svg.append("g")
        .attr("transform", "translate(60, 360)")
        .call(colorLegend);
    
//    svg.call(d3.behavior.zoom().on("zoom", colorLegend));
    
    // fill dataset in appropriate format
    csvdata1.forEach(function(item){ //
        // item example value ["USA", 70]
        var iso = item.iso3c,
                value = item.total_msw_total_msw_generated_tons_year;
        dataset[iso] = { total_msw: value, fillColor: paletteScale(value) };
    });

myMap.updateChoropleth(dataset);
}
);
    
    
    // render map
    var myMap = new Datamap({
        element: document.getElementById('container1'),
        projection: 'mercator', // big world map
//        done: function(datamap){
//            datamap.svg.call(d3.behavior.zoom().on("zoom", redraw));
//            function redraw() {
//                datamap.svg.selectAll("g").attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
//            }
//        },
        // countries don't listed in dataset will be painted with this color
        fills: { defaultFill: '#FFFFFF'},
        data: dataset,
        geographyConfig: {
            borderColor: '#DEDEDE',
            highlightBorderWidth: 2,
            // don't change color on mouse hover
            highlightFillColor: function(geo) {
                return geo['fillColor'] || '#F5F5F5';
            },
            // only change border
            highlightBorderColor: '#B7B7B7',
            // show desired information in tooltip
            popupTemplate: function(geo, data) {
                // don't show tooltip if country don't present in dataset
                if (!data) { 
                    return ['<div class="hoverinfo">',
                    '<strong>', geo.properties.name, '</strong>',
                    '<br>Total msw: Unknown <strong>', '</strong>',
                    '</div>'].join('');
                }
                // tooltip content
                return ['<div class="hoverinfo">',
                    '<strong>', geo.properties.name, '</strong>',
                    '<br>Total msw: <strong>', (data.total_msw/1000000).toFixed(2), ' Mt tons</strong>',
                    '</div>'].join('');
            }
        }
    });
    

    
</script>

</body>