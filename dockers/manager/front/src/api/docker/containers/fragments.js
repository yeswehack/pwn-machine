import gql from "graphql-tag";

export const PROCESS_FRAGMENT = gql`
  fragment ProcessFragment on DockerContainerProcess {
    user
    pid
    cpu
    mem
    vsz
    rss
    tty
    stat
    start
    time
    command
  }
`;

export const MOUNT_FRAGMENT = gql`
  fragment MountFragment on DockerContainerMount {
    type
    name
    source
    target
    readonly
  }
`;

export const EXPOSED_PORTS_FRAGMENT = gql`
  fragment ExposedPortFragment on DockerContainerPort {
    protocol
    containerPort
    targets
  }
`;

export const CONNECTION_FRAGMENT = gql`
  fragment ConnectionFragment on DockerContainerConnection {
    aliases
    ipAddress
    network {
      id
      name
    }
  }
`;

export const CONTAINER_FRAGMENT = gql`
  fragment ContainerFragment on DockerContainer {
    id
    name
    status
    command
    privileged

    labels {
      key
      value
    }
    image {
      id
      shortId
      name
    }
    environment {
      key
      value
    }
    mounts {
      ...MountFragment
    }
    connections {
      ...ConnectionFragment
    }
    ports {
      ...ExposedPortFragment
    }
    ps {
      ...ProcessFragment
    }
  }
  ${MOUNT_FRAGMENT}
  ${PROCESS_FRAGMENT}
  ${EXPOSED_PORTS_FRAGMENT}
  ${CONNECTION_FRAGMENT}
`;
