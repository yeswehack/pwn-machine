
import gql from "graphql-tag";
import { networkFragment } from "./fragments.js"


export const createDockerNetwork = gql` 
mutation createDockerNetwork($name:String!, $internal: Boolean, $gateway: String, $subnet: String, $labels: [LabelInput]) {
    createDockerNetwork(name: $name, internal: $internal, gateway: $gateway, subnet: $subnet, labels: $labels) {
        network {
            ...networkFragment
        }
    }
}
${networkFragment}
`

export const deleteDockerNetwork = gql` 
mutation deleteDockerNetwork($name:String!) {
    deleteDockerNetwork(name: $name) {
        ok
    }
}
`

export const detachContainerFromDockerNetwork = gql`
mutation detachContainerFromDockerNetwork($network: String!, $container: String!){
    detachContainerFromDockerNetwork(network: $network, container:$container){
        network {
            ...networkFragment
        }
    }
}
${networkFragment}
` 

export const attachContainerToDockerNetwork = gql`
mutation attachContainerToDockerNetwork($network: String!, $container: String!){
    attachContainerToDockerNetwork(network: $network, container:$container){
        network {
            ...networkFragment
        }
    }
}
${networkFragment}
` 