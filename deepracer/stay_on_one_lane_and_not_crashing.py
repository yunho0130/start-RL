def reward_function(params):

    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    objects_distance = params['objects_distance']
    _, next_object_index = params['closest_objects']
    objects_left_of_center = params['objects_left_of_center']
    is_left_of_center = params['is_left_of_center']

    # 0에 가깝지만 0이 아닌 초기 보상 설정
    # 0은 오프 트랙 또는 충돌에 해당
    reward = 1e-3

    # 차량이 트랙 경계선 내에 있으면 보상 부여
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward_lane = 1.0
    else:
        reward_lane = 1e-3

    # 차량이 다음 객체에 너무 가까우면 페널티 부여
    reward_avoid = 1.0

    # 다음 객체까지의 거리
    distance_closest_object = objects_distance[next_object_index]
    # 차량과 다음 객체가 같은 차선에 있는지 판정
    is_same_lane = objects_left_of_center[next_object_index] == is_left_of_center

    if is_same_lane:
        if 0.5 <= distance_closest_object < 0.8: 
            reward_avoid *= 0.5
        elif 0.3 <= distance_closest_object < 0.5:
            reward_avoid *= 0.2
        elif distance_closest_object < 0.3:
            reward_avoid = 1e-3 # 거의 부딪힌 경우

    # 위 2가지 요소에 가중치를 부여하고 합산하여 보상 계산
    reward += 1.0 * reward_lane + 4.0 * reward_avoid

    return reward