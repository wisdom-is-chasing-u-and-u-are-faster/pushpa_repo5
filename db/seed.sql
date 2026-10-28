-- Baseline Seed Data for Smart Study Management System

-- Users
INSERT OR IGNORE INTO users (id, name, email, password_hash, role) VALUES
('usr_alex_001', 'Alex Morgan', 'alex@smartstudy.edu', 'password123', 'student'),
('usr_maria_002', 'Maria Garcia', 'maria@smartstudy.edu', 'password123', 'student'),
('usr_david_003', 'David Kim', 'david@smartstudy.edu', 'password123', 'student'),
('usr_emily_004', 'Emily Davis', 'emily@smartstudy.edu', 'password123', 'student'),
('usr_chen_005', 'Dr. Chen', 'chen@smartstudy.edu', 'password123', 'faculty');

-- Syllabi
INSERT OR IGNORE INTO syllabi (id, course_code, course_title, term, status) VALUES
('syl_cs301', 'CS301', 'Algorithm Analysis & Design', 'Fall 2026', 'PROCESSED'),
('syl_bio210', 'BIO210', 'Cellular & Molecular Biology', 'Fall 2026', 'PROCESSED'),
('syl_math105', 'MATH105', 'Multivariable Calculus & Linear Algebra', 'Fall 2026', 'PROCESSED');

-- Syllabus Topics
INSERT OR IGNORE INTO syllabus_topics (id, syllabus_id, topic_name, order_index) VALUES
('top_001', 'syl_cs301', 'Dynamic Programming & Memoization', 1),
('top_002', 'syl_cs301', 'Graph Traversal & Shortest Path', 2),
('top_003', 'syl_cs301', 'NP-Completeness & Approximation', 3),
('top_004', 'syl_bio210', 'Cellular Respiration & Krebs Cycle', 1),
('top_005', 'syl_bio210', 'DNA Replication & Gene Expression', 2),
('top_006', 'syl_math105', 'Partial Derivatives & Gradients', 1),
('top_007', 'syl_math105', 'Eigenvalues & Matrix Transformations', 2);

-- Study Blocks for Student Alex
INSERT OR IGNORE INTO study_blocks (id, user_id, course_code, topic, time_range, duration_minutes, cognitive_load, status, schedule_date) VALUES
('blk_001', 'usr_alex_001', 'CS301', 'Dynamic Programming & Complexity', '9:00 AM - 10:30 AM', 90, 'High', 'Pending', '2026-07-23'),
('blk_002', 'usr_alex_001', 'BIO210', 'Cellular Respiration & ATP Synthesis', '11:00 AM - 12:00 PM', 60, 'Medium', 'Pending', '2026-07-23'),
('blk_003', 'usr_alex_001', 'MATH105', 'Eigenvectors & Diagnostic Review', '2:00 PM - 2:30 PM', 30, 'Low', 'Completed', '2026-07-23');

-- Student Progress & Metrics
INSERT OR IGNORE INTO student_metrics (id, user_id, course, weekly_hours_target, hours_completed, adherence_rate, velocity_score, at_risk) VALUES
('met_001', 'usr_alex_001', 'CS301', 20.0, 16.5, 82.5, 1.15, 0),
('met_002', 'usr_maria_002', 'BIO210', 18.0, 17.0, 94.4, 1.30, 0),
('met_003', 'usr_david_003', 'MATH105', 20.0, 9.5, 47.5, 0.65, 1),
('met_004', 'usr_emily_004', 'CS301', 15.0, 13.5, 90.0, 1.10, 0);

-- Quizzes
INSERT OR IGNORE INTO quizzes (id, user_id, course_code, topic, difficulty, question_count) VALUES
('quiz_sample_001', 'usr_alex_001', 'CS301', 'Dynamic Programming', 'Medium', 3),
('quiz_sample_002', 'usr_alex_001', 'BIO210', 'Cellular Respiration', 'Easy', 2);

-- Questions
INSERT OR IGNORE INTO quiz_questions (id, quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, explanation) VALUES
('q_001', 'quiz_sample_001', 'What is the primary condition for applying Dynamic Programming?', 'Linear time complexity', 'Overlapping subproblems and optimal substructure', 'Greedy choice property', 'Randomized pivot selection', 'B', 'Dynamic Programming requires both overlapping subproblems and optimal substructure.'),
('q_002', 'quiz_sample_001', 'Which data structure is typically used for Memoization?', 'Hash Map / Array', 'Min Heap', 'Disjoint Set', 'Suffix Tree', 'A', 'Hash Maps or indexed arrays provide O(1) retrieval for memoized state results.'),
('q_003', 'quiz_sample_001', 'What is the time complexity of 0/1 Knapsack with N items and capacity W?', 'O(N log N)', 'O(N * W)', 'O(2^N)', 'O(W^2)', 'B', 'Using standard dynamic programming table, the time complexity is O(N * W).'),
('q_004', 'quiz_sample_002', 'Where does the Krebs cycle take place in eukaryotic cells?', 'Cytosol', 'Mitochondrial matrix', 'Nucleolus', 'Endoplasmic reticulum', 'B', 'The Krebs cycle takes place in the mitochondrial matrix in eukaryotes.'),
('q_005', 'quiz_sample_002', 'What is the primary net ATP yield per glucose molecule during aerobic cellular respiration?', '2 ATP', '4 ATP', '30 to 32 ATP', '64 ATP', 'C', 'Under standard aerobic conditions, oxidative phosphorylation yields approximately 30-32 ATP.');

-- Quiz Submissions History
INSERT OR IGNORE INTO quiz_submissions (id, quiz_id, user_id, score_percent, correct_count, total_questions, diagnostic_feedback) VALUES
('sub_001', 'quiz_sample_001', 'usr_alex_001', 85.0, 3, 3, 'Strong conceptual mastery of optimal substructure and state memoization.'),
('sub_002', 'quiz_sample_002', 'usr_alex_001', 90.0, 2, 2, 'Excellent recall of metabolic pathways and ATP yield calculations.');
