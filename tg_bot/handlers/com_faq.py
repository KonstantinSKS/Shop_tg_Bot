

# @choice_city_router.inline_query(Registration.city)
# @choice_city_router.inline_query(ChangeUserData.change_city)
# async def choice_city(inline_query: types.InlineQuery):
#     """Выбор вариантов города"""
#     await inline_query_handler(inline_query, db.City_db)

# async def inline_query_handler(inline_query: types.InlineQuery,
#                                db_model: db.AsyncDatabaseOperationsWithName):
#     """Общий обработчик для выбора вариантов из inline поиска"""
#     query = inline_query.query

#     if not query:
#         #  получаю все варианты
#         results_from_db = await db_model.get_all_objects()
#     else:
#         #  получаю варианты, которые начинаются на указанную строку
#         results_from_db = await db_model.search_name(name=query)

#     results = []
#     for index, result in enumerate(results_from_db, start=1):
#         results.append(types.InlineQueryResultArticle(
#             id=str(uuid4()),
#             title=result.name,
#             input_message_content=types.InputTextMessageContent(
#                 message_text=result.name
#             )
#         ))
#         if index >= 50:
#             break
#     await inline_query.answer(results, cache_time=1)
