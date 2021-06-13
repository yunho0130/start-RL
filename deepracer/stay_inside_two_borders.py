def reward_function(params):
    
    # 딥레이서 관련 파라미터 읽어오기
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # 0에 가까운 기본 보상
    reward = 1e-3

    # 바퀴가 트랙을 벗어나지 않고 차량이 트랙 경계선 내에 있어면 높은 보상 부여
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # float값을 반환 
    return float(reward)