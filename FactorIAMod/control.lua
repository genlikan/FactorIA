local json = require("json")

local function write_to_file(filename, data)
    game.write_file(filename, data, false)
end

local function get_player_name()
    local player = game.players[1]
    local player_name = player.name
    write_to_file("player_name.json", json.encode(player_name))
end

local function get_inventory()
    local player = game.players[1]
    local inventory = player.get_main_inventory().get_contents()
    write_to_file("player_inventory.json", json.encode(inventory))
end

local function get_all_items()
    local items = {}
    for name, item in pairs(game.item_prototypes) do
        table.insert(items, name)
    end
    write_to_file("all_items.json", json.encode(items))
end

local function get_all_items_info()
    local items = {}
    for name, item in pairs(game.item_prototypes) do
        local item_info = {
            name = item.name,
            type = item.type,
            subgroup = item.subgroup.name,
            stack_size = item.stack_size,
            fuel_value = item.fuel_value,
            place_result = item.place_result and item.place_result.name or nil,
            place_as_tile_result = item.place_as_tile_result and item.place_as_tile_result.result.name or nil,
            localised_name = item.localised_name,
            localised_description = item.localised_description,
        }
        items[name] = item_info
    end
    write_to_file("all_items_info.json", json.encode(items))
end

local function get_recipe(item_name)
    local recipe = game.recipe_prototypes[item_name]
    if recipe then
        local result_count = 1 -- Default to 1 if not specified
        local recipe_info = {
            item_name = item_name,
            result_count = result_count,
            ingredients = {}
        }
        for _, product in pairs(recipe.products) do
            if product.name == item_name then
                recipe_info.result_count = product.amount
                recipe_info.item_name = product.name
            end
        end
        for _, ingredient in pairs(recipe.ingredients) do
            table.insert(recipe_info.ingredients, {
                name = ingredient.name,
                amount = ingredient.amount
            })
        end
        game.write_file("recipe.json", game.table_to_json(recipe_info), false)
    else
        game.write_file("recipe.json", "Recipe not found for item: " .. item_name, false)
    end
end


local function get_technologies()
    local player = game.players[1]
    local technologies = {}
    for name, tech in pairs(player.force.technologies) do
        if tech.researched then
            table.insert(technologies, name)
        end
    end
    write_to_file("technologies.json", json.encode(technologies))
end

local function get_all_technologies()
    local all_technologies = {}
    for name, tech in pairs(game.technology_prototypes) do
        table.insert(all_technologies, name)
    end
    write_to_file("all_technologies.json", json.encode(all_technologies))
end

local function get_technology_info(tech_name)
    local tech = game.players[1].force.technologies[tech_name]
    if tech then
        local prerequisites = {}
        for _, prerequisite in pairs(tech.prerequisites) do
            table.insert(prerequisites, prerequisite.name)
        end
        
        local tech_info = {
            name = tech.name,
            researched = tech.researched,
            level = tech.level,
            prerequisites = prerequisites,
            enabled = tech.enabled
        }
        write_to_file("technology_info.json", json.encode(tech_info))
    else
        write_to_file("technology_info.json", "Technology not found: " .. tech_name)
    end
end

commands.add_command("get_player_name", "Get player's name", function()
    game.print("Model Connection Achieved!")
    get_player_name()
end)

commands.add_command("get_inventory", "Get player's inventory", function()
    get_inventory()
end)

commands.add_command("get_all_items", "Get all items", function()
    get_all_items()
end)

commands.add_command("get_all_items_info", "Get all items info", function()
    get_all_items_info()
end)

commands.add_command("get_recipe", "Get item recipe", function(event)
    get_recipe(event.parameter)
end)

commands.add_command("get_technologies", "Get player's technologies", function()
    get_technologies()
end)

commands.add_command("get_all_technologies", "Get all possible technologies in the game", function()
    get_all_technologies()
end)

commands.add_command("get_technology_info", "Get information about a technology", function(event)
    get_technology_info(event.parameter)
end)

script.on_init(function()
    game.print("FactorIA Mod Initialized")
end)

script.on_load(function()
    game.print("FactorIA Mod Loaded!")
end)

