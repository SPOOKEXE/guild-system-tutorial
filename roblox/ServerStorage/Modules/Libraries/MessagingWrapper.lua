
local MessagingService = game:GetService('MessagingService')

local function returnTrue()
	return true
end

-- // Module // --
local Module = {}

function Module.Publish( topic : string, message : any )
	MessagingService:PublishAsync(topic, message)
end

function Module.PublishAsync( topic : string, message : any )
	task.spawn(function()
		MessagingService:PublishAsync(topic, message)
	end)
end

function Module.SubscribeOnceFilter( topic : string, filter : (...any?) -> nil, callback : (...any?) -> nil ) : RBXScriptConnection?
	local connection; connection = MessagingService:SubscribeAsync(topic, function(...)
		if not filter(...) then
			return
		end
		if connection.Connected then
			connection:Disconnect()
		end
		callback(...)
	end)
	return connection
end

function Module.SubscribeFilter( topic, filter : (...any?) -> boolean , callback : (...any?) -> nil ) : RBXScriptConnection
	return MessagingService:SubscribeAsync(topic, function(...)
		if filter(...) then
			callback(...)
		end
	end)
end

function Module.Subscribe( topic, callback ) : RBXScriptConnection
	return Module.SubscribeFilter(topic, returnTrue, callback)
end

function Module.SubscribeOnce( topic : string, callback : (...any?) -> nil ) : RBXScriptConnection?
	return Module.SubscribeOnceFilter(topic, returnTrue, callback)
end

return Module
