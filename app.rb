# Usage: redis-cli publish message hello

require 'sinatra'
require 'redis'
require 'thin'
require 'tilt/erubis'

set :bind, '0.0.0.0'
conns = []

get '/' do
  erb :index
end

get '/subscribe' do
  content_type 'text/event-stream'
  stream(:keep_open) do |out|
    conns << out
    out.callback { conns.delete(out) }
  end
end

Thread.new do
  redis_url = ENV["REDISTOGO_URL"] # || "redis://localhost:6379"
  uri = URI.parse(redis_url)
  set :redis, Redis.new(:host => uri.host, :port => uri.port, :password => uri.password)

  settings.redis.psubscribe('count', 'count.*') do |on|
    on.pmessage do |match, channel, count|
      channel = channel.sub('count.', '')

      conns.each do |out|
        out << "event: #{channel}\n\n"
        out << "data: #{count}\n\n"
      end
    end
  end
end
