<h1 align="center">Agent Nebula</h1>

<p align="center">
<img src="https://img.shields.io/badge/License-Apache_2.0-brightgreen.svg">
<img src="https://img.shields.io/github/languages/top/ostorlab/agent_nebula">
<img src="https://img.shields.io/github/stars/ostorlab/agent_nebula">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
</p>

_The Nebula Agent is responsible for persisting all types of messages locally._

---

<p align="center">
<img src="https://github.com/ostorlab/agent_nebula/blob/main/images/logo.png" alt="agent-nebula" />
</p>

## Getting Started
To perform your first scan, simply run the following command:
```shell
ostorlab scan run --install --agent agent/ostorlab/nebula link --url www.yourdomain.com --method GET
``` 

This command will download and install `agent/ostorlab/nebula` and target `www.yourdomain.com` with the `GET` method.
For more information, please refer to the [Ostorlab Documentation](https://github.com/Ostorlab/ostorlab/blob/main/README.md)


## Usage

Agent Nebula can be installed directly from the ostorlab agent store or built from this repository.

 ### Install directly from ostorlab agent store

 ```shell
 ostorlab agent install agent/ostorlab/nebula
 ```

You can then run the agent with the following command:
```shell
ostorlab scan run --agent agent/ostorlab/nebula link --url www.yourdomain.com --method GET
```


### Build directly from the repository

 1. To build nebula agent you need to have [ostorlab](https://pypi.org/project/ostorlab/) installed in your machine. If you have already installed ostorlab, you can skip this step.

```shell
pip3 install ostorlab
```

 2. Clone this repository.

```shell
git clone https://github.com/Ostorlab/agent_nebula.git && cd agent_nebula
```

 3. Build the agent image using ostorlab cli.

 ```shell
 ostorlab agent build --file=ostorlab.yaml
 ```

 You can pass the optional flag `--organization` to specify your organisation. The organization is empty by default.

 4. Run the agent using on of the following commands:
	 * If you did not specify an organization when building the image:
    ```shell
    ostorlab scan run --agent agent//nebula ip 8.8.8.8
    ```
	 * If you specified an organization when building the image:
    ```shell
    ostorlab scan run --agent agent/[ORGANIZATION]/nebula link --url www.yourdomain.com --method GET
    ```