import React, { Component } from 'react'
import { Container, Header, Checkbox, Form, Select, Button } from 'semantic-ui-react'

import { VictoryLine, VictoryBar, VictoryChart, VictoryAxis, VictoryTheme } from 'victory'

const data = [
	{x:1, y: 13000},
	{x:2, y: 16500},
	{x:3, y: 14250},
	{x:4, y: 19000}
];

const stockOptions = [
    { key: 'BTC-USD', text: 'Bitcoin (BTC-USD)', value: 'BTC-USD' },
    { key: 'AAPL', text: 'Apple (AAPL)', value: 'AAPL' },
    { key: 'MSFT', text: 'Microsoft (MSFT)', value: 'MSFT' },
    { key: 'INTC', text: 'Intel (INTC)', value: 'INTC' },
  ]

const MODELS = ['gboost', 'ridge', 'lasso', 'nn_1d_lstm']

class AssetForm extends Component {
    state = {
      models: MODELS.reduce(
        (models, model) => ({
          ...models,
	  [model]: false,
        }),
	{}
      ),
      stock: '',
    }
    handleSelect = (e, {value}) => this.setState({ 'stock': value }) // Select stock to predict
    //handleChange = (e, {value}) => this.setState({ [model]: value }) // checkbox ML models
    handleChange = e => {
      e.persist();
      const { name } = e.target;
      console.log(name);

      this.setState(prevState => ({
        models: {
          ...prevState.models,
          [name]: !prevState.models[name]
        }
      }));
    };
    
    render() {
        return (
            <div className="asset-form">
		<Container text>
                    <Header as='h1'>Machine Learning for Asset Prediction</Header>
			<Form>
			    <Form.Group widths='equal'>
				<Form.Field
				    control={Select}
				    label='Select Asset'
				    options={stockOptions}
				    placeholder='Stock Options'
				    onChange={this.handleSelect}
				/>
			    </Form.Group>
			    <Form.Group>
				<Form.Field>
				  <label>Gradient Boost
				    <input
				      name='gboost'
			              type='checkbox'
		                      checked={this.state.models['gboost']}
		                      onChange={this.handleChange}
				    />
			          </label>
				</Form.Field>
				<Form.Field>
			          <label>Ridge Regression
				    <input
		                      name='ridge'
		                      type='checkbox'
		                      checked={this.state.models['ridge']}
		                      onChange={this.handleChange}
		                    />
		                  </label>
				</Form.Field>
				<Form.Field>
		                  <label>Lasso Regression
		                    <input
		                      name='lasso'
		                      type='checkbox'
		                      checked={this.state.models['lasso']}
		                      onChange={this.handleChange}
		                    />
		                  </label>
				</Form.Field>
				<Form.Field>
		                  <label>Neural Network with 1D Convolutional and LSTM Layers
		                    <input
		                      name='nn_1d_lstm'
		                      type='checkbox'
		                      checked={this.state.models['nn_1d_lstm']}
		                      onChange={this.handleChange}
				    />
			          </label>
				</Form.Field>
			    </Form.Group>
			    <Form.Group>
		              <Form.Field control={Button}>Predict</Form.Field>
			    </Form.Group>
			</Form>

			<VictoryChart domainPadding={20} theme={VictoryTheme.material} >
			  <VictoryLine
			    style={{
			      data: { stroke: "#c43a31" },
			      parent: { border: "1px solid #ccc" }
			    }}
			    data={data}
			  />
			</VictoryChart>

		    </Container>
            </div>
        );
    }
}

export default AssetForm
