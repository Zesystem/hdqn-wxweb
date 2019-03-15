#!/usr/bin/bash

ENV=$1

if [ ! ${ENV} ]
then
    ENV=development
fi

export FLASK_CONFIG=${ENV}