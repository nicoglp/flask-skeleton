#!/usr/bin/env python

def main():
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(epilog=__doc__)
    parser.add_argument('--env', action='store', default='development',
                        help='mode in which the app should run: development, ci, uat or production')
    parser.add_argument('--port', type=int, default=5000, help='port to run on when in local mode')
    args = parser.parse_args()

    print 'Running as {env}'.format(env=args.env)

    import os

    if args.env == 'development':
        os.environ.setdefault("UBIOME_ENVIRONMENT", "development")
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Run App
    from app import service

    if args.env != 'development':
        from flup.server.fcgi import WSGIServer
        WSGIServer(
            application=service,
            bindAddress=service.config.get('SOCKET_UNIX'),
            umask=0,
            debug=False
        ).run()
    else:
        # sandbox mode
        print 'Service is running on {env} mode, go play with it =)'.format(env=args.env)
        print '\n'
        service.run(
            host='127.0.0.1',
            port=args.port,
            debug=True,
            threaded=True)


if __name__ == '__main__':
    main()
