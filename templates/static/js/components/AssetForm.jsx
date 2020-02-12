import React, { Component } from 'react'
import { Container, Header, Form, Select, Button } from 'semantic-ui-react'

import { VictoryLine, VictoryChart, VictoryTheme, VictoryAxis } from 'victory'

const stockOptions = [
	{ key: 'BTC-USD', text: 'Bitcoin (BTC-USD)', value: 'BTC-USD' },
	{ key: 'AAPL', text: 'Apple (AAPL)', value: 'AAPL' },
	{ key: 'MSFT', text: 'Microsoft (MSFT)', value: 'MSFT' },
	{ key: 'INTC', text: 'Intel (INTC)', value: 'INTC' },
]

const MODELS = ['gboost', 'ridge', 'lasso', 'nn_1d_lstm']

/*
const datas = [
	{ date: '10/10', val: 4500 },
	{ date: '10/11', val: 4600 },
	{ date: '10/12', val: 4300 },
	{ date: '10/13', val: 4800 },
	{ date: '10/14', val: 4400 },
]
*/
const datas = [2001,2003,2004,2000,2400]

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
		data: datas,
	}
	handleSelect = (e, { value }) => this.setState({ 'stock': value }) // Select stock to predict

	handleChange = e => {
		e.persist();
		const { name } = e.target;

		this.setState(prevState => ({
			models: {
				...prevState.models,
				[name]: !prevState.models[name]
			}
		}));
	};

	handleFormSubmit = formSubmitEvent => {
		formSubmitEvent.preventDefault();

		const json_data = {
			stock: this.state.stock,
			models: this.state.models
		}
		fetch('/api/', {
			method: 'POST',
			headers: {
				'Content-type': 'application/json',
			},
			body: JSON.stringify(json_data),
		})
			.then(res => res.json())
			.then(res => {
				if (res !== null) {
					console.log(res);
					this.setState({
						data: res.data
						/*
							res.map((x) => ({
								date: x.date,
								val: x.val
							}))
						*/
					});
				} else {
					console.log('else');
				}
			})
	};

	createCheckbox = option => (
		<Form.Field key={option}>
			<label>{option}
				<input
					name={option}
					type='checkbox'
					checked={this.state.models[option]}
					onChange={this.handleChange}
				/>
			</label>
		</Form.Field>
	);
	createCheckboxes = () => MODELS.map(this.createCheckbox);

	render() {
		return (
			<div className="asset-form">
				<Container text>
					<Header as='h1'>Machine Learning for Asset Prediction</Header>
					<Form onSubmit={this.handleFormSubmit}>
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
							{this.createCheckboxes()}
						</Form.Group>
						<Form.Group>
							<Form.Field control={Button}>Predict</Form.Field>
						</Form.Group>
					</Form>

					<VictoryChart domainPadding={20} theme={VictoryTheme.material}>
					<VictoryAxis style={{ tickLabels: { angle: -60 } }} />
					<VictoryAxis dependentAxis />
						<VictoryLine
							style={{
								data: { stroke: "#c43a31" },
								parent: { border: "1px solid #ccc" }
							}}
							animate={{
								duration: 2000,
								onLoad: { duration: 1000 }
							  }}
							data={this.state.data}
							x="date"
							y="val"
						/>
					</VictoryChart>

				</Container>
			</div>
		);
	}
}

export default AssetForm
