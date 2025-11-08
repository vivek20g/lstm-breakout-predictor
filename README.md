# 📊 LSTM Breakout Predictor

**LSTM Breakout Predictor** is a machine learning pipeline designed to **simulate intraday trade execution data** and train an **LSTM model** to classify breakout actions:  
**Long Buy**, **Short Sell**, or **No Action**.

---

## 🧩 Project Structure
- `simulator/` – Generates synthetic trade execution data using historical price data and spread matrices.
- `trainer/` – Trains an LSTM model on the simulated data to predict trade actions.
- `model/` – Stores the trained LSTM model.
- `scalers/` – Stores feature scalers used during training.

---

## ⚙️ Installation Instructions

```bash
# Clone the repository
git clone https://github.com/vivek20g/lstm-breakout-predictor.git
cd lstm-breakout-predictor

# Create a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


📂 Input Data Files
Place the following files in the root directory:

NiftyPriceHistory.xlsx – Historical price data.
Buy-Sell-Spread-Matrix.xlsx – Spread configuration.

The simulator will generate:

simulated_trades.xlsx – Synthetic trade dataset with profit/loss values.


📁 Simulator Folder
Purpose
Generates synthetic trade execution data using historical price data and spread matrices, and calculates profit/loss for each trade.
Key Modules

Reads NiftyPriceHistory.xlsx and Buy-Sell-Spread-Matrix.xlsx.
Simulates trades and computes P&L.
Outputs simulated_trades.xlsx for model training.


📁 Trainer Folder
Purpose
Prepares sequences from simulated data, builds and trains an LSTM model, and evaluates classification performance.
Key Modules

prepare_sequences(...) – Scales features and creates sequences.
build_lstm_model(...) – Constructs multi-input LSTM.
train_model(...) – Trains with early stopping and class weights.
evaluate_model(...) – Confusion matrix and classification report.

Output

Trained LSTM model saved in model/.
Scalers saved in scalers/.


📊 Workflow Architecture
flowchart TD    A[NiftyPriceHistory.xlsx + Buy-Sell-Spread-Matrix.xlsx] --> B[Simulator]    B -->|Generates simulated_trades.xlsx| C[Trainer]    C -->|Trains LSTM model| D[Outputs: model/ + scalers/]#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f {font-family:"trebuchet ms", verdana, arial, sans-seriffont-size:16px;fill:rgb(51, 51, 51);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-animation-slow {stroke-dashoffset:900animation-duration:50s;animation-timing-function:linear;animation-delay:0s;animation-iteration-count:infinite;animation-direction:normal;animation-fill-mode:none;animation-play-state:running;animation-name:dash;animation-timeline:auto;animation-range-start:normal;animation-range-end:normal;stroke-linecap:round;stroke-dasharray:9, 5;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-animation-fast {stroke-dashoffset:900animation-duration:20s;animation-timing-function:linear;animation-delay:0s;animation-iteration-count:infinite;animation-direction:normal;animation-fill-mode:none;animation-play-state:running;animation-name:dash;animation-timeline:auto;animation-range-start:normal;animation-range-end:normal;stroke-linecap:round;stroke-dasharray:9, 5;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .error-icon {fill:rgb(85, 34, 34)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .error-text {fill:rgb(85, 34, 34)stroke:rgb(85, 34, 34);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-thickness-normal {stroke-width:1px}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-thickness-thick {stroke-width:3.5px}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-pattern-solid {stroke-dasharray:0}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-thickness-invisible {stroke-width:0fill:none;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-pattern-dashed {stroke-dasharray:3}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-pattern-dotted {stroke-dasharray:2}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .marker {fill:rgb(51, 51, 51)stroke:rgb(51, 51, 51);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .marker.cross {stroke:rgb(51, 51, 51)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f svg {font-family:"trebuchet ms", verdana, arial, sans-seriffont-size:16px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f p {margin-top:0pxmargin-right:0px;margin-bottom:0px;margin-left:0px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .label {font-family:"trebuchet ms", verdana, arial, sans-serifcolor:rgb(51, 51, 51);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster-label text {fill:rgb(51, 51, 51)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster-label span {color:rgb(51, 51, 51)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster-label span p {background-color:transparent}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .label text, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f span {fill:rgb(51, 51, 51)color:rgb(51, 51, 51);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node rect, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node circle, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node ellipse, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node polygon, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node path {fill:rgb(236, 236, 255)stroke:rgb(147, 112, 219);stroke-width:1px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .rough-node .label text, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .label text, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape .label, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape .label {text-anchor:middle}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .katex path {fill:rgb(0, 0, 0)stroke:rgb(0, 0, 0);stroke-width:1px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .rough-node .label, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .label, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape .label, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape .label {text-align:center}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node.clickable {cursor:pointer}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .root .anchor path {stroke-width:0stroke:rgb(51, 51, 51);fill:rgb(51, 51, 51);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .arrowheadPath {fill:rgb(51, 51, 51)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgePath .path {stroke:rgb(51, 51, 51)stroke-width:2px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .flowchart-link {stroke:rgb(51, 51, 51)fill:none;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgeLabel {background-color:rgba(232, 232, 232, 0.8)text-align:center;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgeLabel p {background-color:rgba(232, 232, 232, 0.8)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgeLabel rect {opacity:0.5background-color:rgba(232, 232, 232, 0.8);fill:rgba(232, 232, 232, 0.8);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .labelBkg {background-color:rgba(232, 232, 232, 0.5)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster rect {fill:rgb(255, 255, 222)stroke:rgb(170, 170, 51);stroke-width:1px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster text {fill:rgb(51, 51, 51)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster span {color:rgb(51, 51, 51)}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f div.mermaidTooltip {position:absolutetext-align:center;max-width:200px;padding-top:2px;padding-right:2px;padding-bottom:2px;padding-left:2px;font-family:"trebuchet ms", verdana, arial, sans-serif;font-size:12px;background-image:initial;background-position-x:initial;background-position-y:initial;background-size:initial;background-repeat:initial;background-attachment:initial;background-origin:initial;background-clip:initial;background-color:rgb(249, 255, 236);border-top-width:1px;border-right-width:1px;border-bottom-width:1px;border-left-width:1px;border-top-style:solid;border-right-style:solid;border-bottom-style:solid;border-left-style:solid;border-top-color:rgb(170, 170, 51);border-right-color:rgb(170, 170, 51);border-bottom-color:rgb(170, 170, 51);border-left-color:rgb(170, 170, 51);border-image-source:initial;border-image-slice:initial;border-image-width:initial;border-image-outset:initial;border-image-repeat:initial;border-top-left-radius:2px;border-top-right-radius:2px;border-bottom-right-radius:2px;border-bottom-left-radius:2px;pointer-events:none;z-index:100;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .flowchartTitleText {text-anchor:middlefont-size:18px;fill:rgb(51, 51, 51);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f rect.text {fill:nonestroke-width:0;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape {background-color:rgba(232, 232, 232, 0.8)text-align:center;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape p, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape p {background-color:rgba(232, 232, 232, 0.8)padding-top:2px;padding-right:2px;padding-bottom:2px;padding-left:2px;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape rect, #mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape rect {opacity:0.5background-color:rgba(232, 232, 232, 0.8);fill:rgba(232, 232, 232, 0.8);}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .label-icon {display:inline-blockheight:1em;overflow-x:visible;overflow-y:visible;vertical-align:-0.125em;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .label-icon path {fill:currentcolorstroke:revert;stroke-width:revert;}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f :root {--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif}
#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .error-icon{fill:#552222;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .error-text{fill:#552222;stroke:#552222;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-thickness-normal{stroke-width:1px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-thickness-thick{stroke-width:3.5px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-pattern-solid{stroke-dasharray:0;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .marker{fill:#333333;stroke:#333333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .marker.cross{stroke:#333333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f p{margin:0;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster-label text{fill:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster-label span{color:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster-label span p{background-color:transparent;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .label text,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f span{fill:#333;color:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node rect,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node circle,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node ellipse,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node polygon,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .rough-node .label text,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .label text,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape .label,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape .label{text-anchor:middle;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .rough-node .label,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .label,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape .label,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape .label{text-align:center;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node.clickable{cursor:pointer;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .root .anchor path{fill:#333333!important;stroke-width:0;stroke:#333333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .arrowheadPath{fill:#333333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgePath .path{stroke:#333333;stroke-width:2.0px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .flowchart-link{stroke:#333333;fill:none;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgeLabel{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgeLabel p{background-color:rgba(232,232,232, 0.8);}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .edgeLabel rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster text{fill:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .cluster span{color:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f rect.text{fill:none;stroke-width:0;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape p,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape p{background-color:rgba(232,232,232, 0.8);padding:2px;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .icon-shape rect,#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .image-shape rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-e772620f-7188-49cd-9d8f-b0519b8dea8f :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}Generates simulated_trades.xlsxTrains LSTM modelNiftyPriceHistory.xlsx +Buy-Sell-Spread-Matrix.xlsxSimulatorTrainerOutputs: model/ + scalers/Show more lines

✅ Summary

Model: Multi-input LSTM using TensorFlow/Keras.
Signals: Long Buy, Short Sell, or No Action.
Data: Synthetic trade data generated from historical prices and spread matrices.


📬 Contact
For questions or contributions, please reach out via GitHub Issues or Pull Requests.
