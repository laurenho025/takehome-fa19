import React, { Component } from 'react'
import Instructions from './Instructions'
import Contact from './Contact'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      contacts: [
        {id: 1, name: "Angad", nickname: "greg", hobby: "dirty-ing"},
        {id: 2, name: "Roy", nickname: "uwu", hobby: "weeb"},
        {id: 3, name: "Daniel", nickname: "oppa", hobby: "losing money with options trading"},
      ],
      inputContact: "",
      count: 0,
    }
  }

  componentWillMount() {
    let updateCount = this.state.contacts.length;
    this.setState({
      count: updateCount,
    });
  }

  onChange = event => {
    this.setState({
      inputContact: event.target.value
    });
  }

  addContact() {
    let newContacts = this.state.contacts;
    newContacts.push({
      id: newContacts.length + 1,
      name: this.state.inputContact,
      nickname: "bob",
      hobby: "boolin",
    });

    this.setState({
      contacts: newContacts,
      inputContact: "",
      count: this.state.count + 1,
    });
  }

  render() {
    return (
      <div className="App">
        <Instructions complete={true} />

        {this.state.contacts.map(x => (
          <Contact id={x.id} name={x.name} nickcname={x.nickname} hobby={x.hobby} />
        ))}

        <Counter count={this.state.count} />
        <input
          type="text"
          placeholder="Add Contact"
          value={this.state.inputContact}
          onChange={this.onChange}
        />
        <button onClick={this.addContact.bind(this)}>Submit</button>
      </div>
    )
  }
}

export default App
