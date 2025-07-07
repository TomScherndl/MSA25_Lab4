FROM public.ecr.aws/docker/library/python:3.12-slim

# Update and upgrade system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# INFO: args can be supplied via docker build
# they are used as a best-practise, that the docker image does not run using the root user
ARG buildtime_variable_username="containeruser"
ARG buildtime_variable_groupname="containergroup"
ARG buildtime_variable_uid="65532"
ARG buildtime_variable_gid="65532"

# define your appliction working directory
ARG buildtime_application_dir="/opt/streamlit_dashboard"
WORKDIR ${buildtime_application_dir}

COPY requirements.txt .
RUN pip install -r ./requirements.txt
## copy the relevant files to the workdir
COPY . . 

# Do not run as root user
# debian specific user/group creation
RUN groupadd -r -g ${buildtime_variable_gid} ${buildtime_variable_groupname} \
    && useradd -rM -d ${buildtime_application_dir} -s /sbin/nologin -g ${buildtime_variable_gid} -u ${buildtime_variable_uid} ${buildtime_variable_username}
RUN chown ${buildtime_variable_uid}:${buildtime_variable_gid} ${buildtime_application_dir}

# run the process with the defined user
USER ${buildtime_variable_username}

# define a listening port: e.g. 8080
EXPOSE 8080

# use the defined appliction-directory and the main python file
# Build a shell script because the ENTRYPOINT command doesn't like using ENV
RUN echo "#!/bin/bash \n streamlit run ${buildtime_application_dir}/Welcome.py --server.port=8080 --server.address=0.0.0.0" > ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Run the generated shell script.
ENTRYPOINT ["./entrypoint.sh"]