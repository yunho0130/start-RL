def reward_function(params):
    
    # 딥레이서 관련 파라미터 읽어오기
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle

    # 중앙선으로부터 거리에 따라 마커 3개를 설정
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # 차량이 중앙선에 가까우면 보상을 크게, 멀면 보상을 작게
    if distance_from_center <= marker_1:
        reward = 1
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # 거의 부딪히거나 트랙 이탈에 가까운 경우

    # 조향 임곗값 설정. 행동 공간 설정에 따라 값을 바꿔 주어야 함
    ABS_STEERING_THRESHOLD = 15

    # 조향 각도가 너무 크면 페널티 부여
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)