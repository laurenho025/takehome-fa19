import React, { Component } from 'react'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      id: this.props.id,
      name: this.props.name,
      hobby: this.props.hobby,
    }
  }
  
  render() {
    return (
      <div>
        <p>Name: {this.state.name}</p>
      </div>
    )
  }
}

export default App
