# Alpha v0.0.1

Alpha is the project name assigned to goal of implementing a distributed, micro-service based design architecture for creating versatile, resilient, and scalable web applications with Python Django.

Considerations throughout the development of this solution have been the accommodation of:

1. multiple deployment configurations
   * services must support a highly available configuration i.e. replication
   * services must be de-coupled i.e. the ability to scale service *A*, must not depend on the state of service *B*

2. multiple deployment environments
   * for each service there must exist a mapping to managed cloud services offered by Google Cloud Platform

## Purpose

This package is only intended to provide a starting point for applications which intend to implement a distributed, micro-service design. For more on design and deployment go to [K8s](./k8s/k8s.md)
