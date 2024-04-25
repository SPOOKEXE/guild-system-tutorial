
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local LocalAssets = LocalPlayer:WaitForChild('PlayerScripts'):WaitForChild('Assets')

local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local LocalModules = require(LocalPlayer:WaitForChild("PlayerScripts"):WaitForChild("Modules"))

local UserInterfaceUtility = LocalModules.Utility.UserInterface

local Interface = LocalPlayer:WaitForChild('PlayerGui'):WaitForChild('Interface')

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReplicatedModules = require(ReplicatedStorage:WaitForChild("Modules"))

local GuildsConfigModule = ReplicatedModules.Data.Guilds
local MaidClassModule = ReplicatedModules.Modules.Maid
local ReplicatedData = ReplicatedModules.Services.ReplicatedData

local RNetModule = ReplicatedModules.Libraries.RNet
local GuildsBridge = RNetModule.Create('GuildsBridge')

local SystemsContainer = {}

local function TweenPosition( Frame : Frame, Position : UDim2, duration : number? )
	Frame:TweenPosition( Position, Enum.EasingDirection.InOut, Enum.EasingStyle.Linear, duration or 0.5, true )
end

-- // Module // --
local Module = {}

Module.IsOpen = nil
Module.WidgetMaid = ReplicatedModules.Modules.Maid.New()

Module.IsGuildsAvailable = false

function Module.CreateEmblemFrame( parent : Frame, emblemId : string ) : Frame
	local frame = parent:FindFirstChild(emblemId)
	if not frame then
		frame = LocalAssets.UI.TemplateEmblem:Clone()
		frame.Name = emblemId
		frame.Icon.Image = emblemId
		frame.Parent = parent
	end
	return frame
end

function Module.SelectEmblemFrame( parent : Frame, emblemId : string )
	for _, frame in parent:GetChildren() do
		if frame:IsA('Frame') then
			if frame.Name == emblemId then
				frame.UIStroke.Color = Color3.fromRGB(208, 184, 46)
			else
				frame.UIStroke.Color = Color3.fromRGB(75, 72, 64)
			end
		end
	end
end

function Module.SetupNoGuildFrame()

	local NoGuildFrame : Frame = Interface.NoGuildFrame.Container

	local selectedEmblemIndex : number = -1

	-- create temlate emblems to select
	if #NoGuildFrame.Create.Emblems:GetChildren() == 2 then
		for index, emblemId in GuildsConfigModule.Emblems do
			local frame = Module.CreateEmblemFrame( NoGuildFrame.Create.Emblems, emblemId )
			frame.LayoutOrder = index
			Module.WidgetMaid:Give(frame)
			local button = UserInterfaceUtility.CreateActionButton({Parent = frame})
			button.Activated:Connect(function()
				selectedEmblemIndex = index
				Module.SelectEmblemFrame( NoGuildFrame.Create.Emblems, emblemId )
			end)
			Module.WidgetMaid:Give(button)
		end
	end

	-- create button
	local debounce = false
	Module.WidgetMaid:Give(NoGuildFrame.Create.CreateButton.Activated:Connect(function()
		if debounce then
			return
		end
		debounce = true
		print(NoGuildFrame.Create.NameInput.Text, NoGuildFrame.Create.DescInput.Text, selectedEmblemIndex)
		if selectedEmblemIndex == -1 then
			task.wait(2)
		elseif #NoGuildFrame.Create.NameInput.Text < 3 or #NoGuildFrame.Create.NameInput.Text > 12 then
			NoGuildFrame.Create.NameInput.PlaceholderColor3 = Color3.fromRGB(255, 255, 255)
			NoGuildFrame.Create.NameInput.TextColor3 = Color3.fromRGB(255, 255, 255)
			task.wait(2)
			NoGuildFrame.Create.NameInput.PlaceholderColor3 = Color3.fromRGB(178, 171, 114)
			NoGuildFrame.Create.NameInput.TextColor3 = Color3.fromRGB(236, 236, 236)
		elseif #NoGuildFrame.Create.DescInput.Text > 100 then
			NoGuildFrame.Create.DescInput.PlaceholderColor3 = Color3.fromRGB(255, 255, 255)
			NoGuildFrame.Create.DescInput.TextColor3 = Color3.fromRGB(255, 255, 255)
			task.wait(2)
			NoGuildFrame.Create.DescInput.PlaceholderColor3 = Color3.fromRGB(178, 171, 114)
			NoGuildFrame.Create.DescInput.TextColor3 = Color3.fromRGB(236, 236, 236)
		else
			local success, err = GuildsBridge:InvokeServer(
				GuildsConfigModule.RemoteEnums.CreateGuild,
				NoGuildFrame.Create.NameInput.Text,
				NoGuildFrame.Create.DescInput.Text,
				selectedEmblemIndex
			)
			NoGuildFrame.Create.CreateButton.Text = err
			NoGuildFrame.Create.CreateButton.TextColor3 = success and Color3.new(0, 0.9, 0) or Color3.new(0.9, 0, 0)
			task.wait(2)
			NoGuildFrame.Create.CreateButton.Text = 'CREATE'
			NoGuildFrame.Create.CreateButton.TextColor3 = Color3.fromRGB(255, 249, 180)
		end
		debounce = false
	end))

end

function Module.UpdateNoGuildFrame()
	-- availability label
	Interface.NoGuildFrame.Container.Visible = Module.IsGuildsAvailable
	Interface.NoGuildFrame.Unavailable.Visible = not Module.IsGuildsAvailable
	if not Module.IsGuildsAvailable then
		return
	end
	print('noGuildFrame')
	-- invites
end

function Module.UpdateMyGuildFrame()
	-- availability label
	Interface.MyGuildFrame.Container.Visible = Module.IsGuildsAvailable
	Interface.MyGuildFrame.Unavailable.Visible = not Module.IsGuildsAvailable
	if not Module.IsGuildsAvailable then
		return
	end

	print('myGuildFrame')

	local playerData = ReplicatedData.GetData('PlayerData', false)
	print(playerData)

	local guildData = ReplicatedData.GetData('GuildData', false)
	print(guildData)
end

function Module.UpdateGuildUI()
	local playerData = ReplicatedData.GetData('PlayerData', false)
	local guildUUID = playerData and playerData.GuildUUID
	Interface.NoGuildFrame.Visible = (guildUUID == nil)
	Interface.MyGuildFrame.Visible = (guildUUID ~= nil)

	if guildUUID == nil then
		TweenPosition( Interface.NoGuildFrame, UDim2.fromScale(0.5, 0.5), nil )
		TweenPosition( Interface.MyGuildFrame, UDim2.fromScale(-0.5, 0.5), nil )
		Module.UpdateNoGuildFrame()
	else
		TweenPosition( Interface.MyGuildFrame, UDim2.fromScale(0.5, 0.5), nil )
		TweenPosition( Interface.NoGuildFrame, UDim2.fromScale(-0.5, 0.5), nil )
		Module.UpdateMyGuildFrame()
	end
end

function Module.OpenWidget()
	if Module.IsOpen then
		return
	end
	Module.IsOpen = true

	Module.IsGuildsAvailable = workspace:GetAttribute('GuildsAvailable')
	Module.WidgetMaid:Give(workspace:GetAttributeChangedSignal('GuildsAvailable'):Connect(function()
		Module.IsGuildsAvailable = workspace:GetAttribute('GuildsAvailable')
		Module.UpdateGuildUI()
	end))

	task.defer(Module.SetupNoGuildFrame)
	task.defer(Module.UpdateGuildUI)
end

function Module.CloseWidget()
	if not Module.IsOpen then
		return
	end
	Module.IsOpen = false

	TweenPosition( Interface.NoGuildFrame, UDim2.fromScale(-0.5, 0.5), nil )
	TweenPosition( Interface.MyGuildFrame, UDim2.fromScale(-0.5, 0.5), nil )

	Module.WidgetMaid:Cleanup()
end

function Module.Start()

	ReplicatedData.OnUpdated:Connect(function(Category, Data)
		if Category == 'PlayerData' and Module.IsOpen then
			Module.UpdateGuildUI()
		elseif Category == 'GuildData' and Module.IsOpen then
			print(Data)
			Module.UpdateMyGuildFrame()
		end
	end)

	Interface.NoGuildFrame.Position = UDim2.fromScale(-0.5, 0.5)
	Interface.NoGuildFrame.Visible = true
	Interface.MyGuildFrame.Position = UDim2.fromScale(-0.5, 0.5)
	Interface.MyGuildFrame.Visible = true

	local debounce = false
	local Button = UserInterfaceUtility.CreateActionButton({Parent = Interface.GuildButton})
	Button.Activated:Connect(function()
		if debounce then
			return
		end
		debounce = true
		if Module.IsOpen then
			Module.CloseWidget()
		else
			Module.OpenWidget()
		end
		task.wait(1)
		debounce = false
	end)

end

function Module.Init(otherSystems)
	SystemsContainer = otherSystems
end

return Module
