# Server for Static Files


## This is the backend for static.linushorn.dev/*

### How to run
1. Clone the repo
2. Build the docker image with `docker build -t static-server .`
3. Run the docker image with `docker run -p [ext_port]:1950 static-server`
4. Done! You can now access the server at `localhost:[ext_port]`