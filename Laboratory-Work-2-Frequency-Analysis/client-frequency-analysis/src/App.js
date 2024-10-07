import './App.css';
import axios from "axios";
import React, { Component } from "react";
import Plot from 'react-plotly.js';

class App extends Component {
  state = {
    selectedFile: null,
    fileContent: "",
    plotData: [],
    plotLayout: {},
    processedLetters: [],
    interceptFrequencies: {
      labels: ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z'],
      values: [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1, 6.0, 4.3, 4.0, 3.4, 2.8, 2.8, 2.4, 2.4, 2.2, 2.0, 2.0, 1.9, 1.5, 1.0, 0.8, 0.15, 0.15, 0.1, 0.07],
    },
    interceptPlotLayout: {},
    userIntercept: {},
    originalFileContent: "",
    digraphsInCipher: [],
    trigraphsInCipher: [],
    digraphsCommon: ["TH","HE","AN","IN","ER","ON","RE","ED","ND","HA","AT","EN"],
    trigraphsCommon: ["THE","AND","THA","ENT","ION","TIO","FOR","NDE","HAS","NCE","TIS","OFT","MEN"],
  };

  onFileChange = (event) => {
    this.setState({
      selectedFile: event.target.files[0]
    });
  };

  onFileUpload = () => {
    if (!this.state.selectedFile) {
      alert("Please select a file first.");
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const fileContent = event.target.result;
      this.setState({ fileContent: fileContent.toUpperCase(), originalFileContent: fileContent });

      const payload = {
        fileContent: fileContent
      };

      axios.post("http://localhost:5000/api/process-cipher-text", payload, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          const plotData = [{
            x: Object.keys(response.data),
            y: Object.values(response.data),
            type: 'bar',
            hovertemplate: '%{y:.2f}%'
          }];
          const plotLayout = {
            title: 'Character Frequency in Cipher Text',
            xaxis: { title: 'Characters' },
            yaxis: { title: 'Occurrences' },
            font: { color: 'white' },
            width: "50%",
            height: "60%",
            paper_bgcolor: '#282c34',
            plot_bgcolor: '#282c34',
          };
          
          // Update processed letters based on the response data keys
          this.setState({ plotData, plotLayout, processedLetters: Object.keys(response.data) });

          this.fetchDigraphs();
          this.fetchTrigraphs();
        })
        .catch(error => {
          console.error("Error uploading the file:", error);
        });
    };
    
    reader.readAsText(this.state.selectedFile);
  };

  fileData = () => {
    if (this.state.selectedFile && !this.state.fileContent) {
      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: {this.state.selectedFile.name}</p>
          <p>File Type: {this.state.selectedFile.type}</p>
          <p>Last Modified: {this.state.selectedFile.lastModifiedDate.toDateString()}</p>
        </div>
      );
    } else if (this.state.fileContent) {
      return (
        <div className="plot-container">
          <Plot data={this.state.plotData} layout={this.state.plotLayout} />
          <Plot
            data={[{
              x: this.state.interceptFrequencies.labels,
              y: this.state.interceptFrequencies.values,
              type: 'bar',
              hovertemplate: '%{y:.2f}%',
            }]}
            layout={{
              title: 'Character Frequency in English Alphabet',
              xaxis: { title: 'Characters' },
              yaxis: { title: 'Frequency (%)' },
              font: { color: 'white' },
              width: "50%",
              height: "60%",
              paper_bgcolor: '#282c34',
              plot_bgcolor: '#282c34',
            }}
          />
        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  };

  handleUserInputChange = (event, char) => {
    const value = event.target.value;
  
    // Check if the value is a single letter (case insensitive) and not empty
    if (/^[A-Za-z]$/.test(value)) {
      this.setState(prevState => ({
        userIntercept: {
          ...prevState.userIntercept,
          [char]: value
        }
      }));
    } else if (value === "") {
      // Prevent empty input by not updating the state
      this.setState(prevState => ({
        userIntercept: {
          ...prevState.userIntercept,
          [char]: '' // Set to empty string only if required
        }
      }));
    }
  };
  
  renderInterceptInputMapping = () => {
    if (this.state.processedLetters.length === 0) return null;
  
    return (
      <div className="intercept-input-container">
        <h4>Modify Intercept Values:</h4>
        <div className="input-row">
          {this.state.processedLetters.map(char => (
            <div key={char} className="input-group">
              <label className="small-label">{char}:</label>
              <input
                type="text"
                value={this.state.userIntercept[char] || ""}
                onChange={(e) => this.handleUserInputChange(e, char)}
                className="input-box"
                maxLength={1} // Limit input to a single character
              />
            </div>
          ))}
        </div>
      </div>
    );
  };

  modifyLetters = () => {
    
    const payload = {
      fileContent: this.state.originalFileContent,
      userIntercept: this.state.userIntercept
    };

    axios.post("http://localhost:5000/api/modify-letters", payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        this.setState({ fileContent: response.data });
      })
      .catch(error => {
        console.error("Error modifying the letters:", error);
      });
  };

  printText = () => {
    if (this.state.originalFileContent) {
      return (
        <div className='div-text'>
          <div className='input-group-text'>
          <label>Intercept:</label>
          <div className='input-row-text'>
            <textarea
              value={this.state.originalFileContent}
              rows={8}
              cols={50}
              readOnly
            />
          </div>
          
          <label>Deciphered Text:</label>
          <textarea
            value={this.state.fileContent}
            rows={8}
            cols={50}
            readOnly
          />
          </div>
          <div className='input-row-text'>
            <button onClick={this.handleReset}>Reset</button>
            <button onClick={this.modifyLetters}>Modify Letters!</button>
          </div>
        </div>
      );
    }
  };
  

  handleReset = () => {
    this.setState({

      fileContent: "",
      userIntercept: {},
      processedLetters: [],
      originalFileContent: "",
      digraphsInCipher: [],
    });
  };

  fetchDigraphs = () => {
    const payload = {
      fileContent: this.state.originalFileContent,
      countGraphs: this.state.digraphsCommon.length,
      countLetters: 2
    };

    // Call the find digraphs API
    axios.post("http://localhost:5000/api/find-graphs", payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        this.setState({ digraphsInCipher: response.data });
      })
      .catch(error => {
        console.error("Error processing digraphs:", error);
      });
  };

  fetchTrigraphs = () => {
    const payload = {
      fileContent: this.state.originalFileContent,
      countGraphs: this.state.trigraphsCommon.length,
      countLetters: 3
    };

    // Call the find digraphs API
    axios.post("http://localhost:5000/api/find-graphs", payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        this.setState({ trigraphsInCipher: response.data });
      })
      .catch(error => {
        console.error("Error processing digraphs:", error);
      });
  };

  renderDigraphs = () => {
    if (this.state.digraphsInCipher.length === 0) return null;

    return (
      <div className="digraph-container">
        <h4>Digraphs:</h4>
        <div className="input_diagraphs">
          <label className="small-label">Common Digraphs in Cipher Text:</label>
          {this.state.digraphsInCipher.map((digraph) => (
            <label className="small-label">{digraph.graph}: {digraph.count}</label>
          ))}
        </div>
        <div className="input_diagraphs">
          <label className="small-label">Common Digraphs in English Language:</label>
          {this.state.digraphsCommon.map((digraph) => (
            <label className="small-label">{digraph}</label>
          ))}
        </div>
      </div>
    );
  };

  renderTrigraphs = () => {
    if (this.state.trigraphsInCipher.length === 0) return null;

    return (
      <div className="digraph-container">
        <h4>Trigraphs:</h4>
        <div className="input_diagraphs">
          <label className="small-label">Common Trigraphs in Cipher Text:</label>
          {this.state.trigraphsInCipher.map((trigraph) => (
            <label className="small-label">{trigraph.graph}: {trigraph.count}</label>
          ))}
        </div>
        <div className="input_diagraphs">
          <label className="small-label">Common Trigraphs in English Language:</label>
          {this.state.trigraphsCommon.map((trigraph) => (
            <label className="small-label">{trigraph}</label>
          ))}
        </div>
      </div>
    );
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Frequency Analyzer</h1>
          <div>
            <input type="file" onChange={this.onFileChange} />
            <button onClick={this.onFileUpload}>Upload!</button>
          </div>
          {this.printText()}
          {this.renderInterceptInputMapping()}

          <div className="digraph-container">
            {this.renderDigraphs()}
            {this.renderTrigraphs()}
          </div>
          {this.fileData()}
        </header>
      </div>
    );
  }
}

export default App;
