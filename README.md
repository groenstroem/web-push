# Grøn strøm web push

This repository contains the logic for creating web push notifications describing the
current emission intensity forecast to all users currently subscribed to notifications.

## Configuration

In order to send messages, we need to specify an email address for the subscriber; i.e.
the administrative contact of the push message, as well as a VAPID private key corresponding
to the public key used when new recipients are subscribed.

## Running

The simplest way to run the script is to use Docker, specifying all configuration parameters
as environment variables, and a Docker volume containing the database of subscriptions.

```
docker build -t groenstroem-web-push .
docker run -v some_volume:/data -e SUB_EMAIL=mail@example.com -e VAPID_KEY=... groenstroem-web-push
```