//! STDIO Jam - Arcade Pig - Leo Tindall
//!
//! This is an "arcade style" Pig game, which can be run persistently in a terminal
//! with multiple players.
//!
//! Because the STDIO Jam rules forbid the use of non-stdout I/O streams, this program
//! retains "high score" information only in memory.

// This _is_ the STDIO Jam after all...
use std::io;
// The current system time is used for seeding the PRNG
use std::time;

// Rust's std:: doesn't provide a random number generator, so here is a
// relatively simple implementation.
/// Produces a number from 1 to sides which is deterministic in seed but otherwise
/// hard to guess.
fn die_roll(seed: u64, sides: u64) -> u64 {

    // seed % range is full range,
    // plus a modification every tick so fewer long runs
    let primary = seed + (seed % (sides + 1));
    // Additional short term noise
    let ripple = (seed % (sides + 1)) + (primary % (sides + 1));
    // Longer term destabilization, applied to every other tick
    let tri = (seed % 32) * (seed % 64) * (seed % 128) * (seed % 2);

    // Combine the three terms and then convert to a die roll
    (primary + ripple + tri) % sides + 1
}

/// Prompt the player for input with the given text.
fn command_line(prompt: &str) -> String {
    // Ask the player for input, based on the given prompt text.
    print!("{}> ", prompt);

    // Explicitly "flush" stdout because it's normally printed
    // line by line.
    use std::io::Write;
    io::stdout().flush().unwrap();

    // Actually read the user's input
    let mut buffer = String::new();
    io::stdin().read_line(&mut buffer).unwrap();

    // Normalize the command so it's easier to work with
    buffer.trim().to_lowercase()
}

/// Not allowed to use a real screen clear, so this just spits out a bunch of
/// newlines.
fn clear_screen() {
    for _ in 0..100 {
        println!("");
    }
}

/// Play a single game of Pig, returning the final score or None if the player
/// aborted prematurely
fn play() -> Option<u64> {

    let mut turns = 0;
    let mut turn_score = 0;
    let mut total_score = 0;


    // Get an unpredictable seed: the time since the epoch, but
    // throwing out everything significant.
    let mut seed_val = time::SystemTime::now()
        .duration_since(time::UNIX_EPOCH)
        .unwrap() // Assumption: It is after Jan 1, 1970
        .subsec_nanos();

    // Print a banner for the player
    println!("Welcome to Pig.");
    println!("Each turn, you can either roll or fold.");
    println!("If you fold, your turn score is added to the total and the turn ends.");
    println!("If you roll, you can increase your score, BUT...");
    println!("if you roll a 1 you lose your whole turn score.");
    println!("Try to get the highest score before 10 turns have passed.");
    println!("----");
    println!("roll or r to roll, fold or f to fold, quit or q to exit");

    // Run until the game is over
    while turns < 5 {
        // Inform the player about the current state of the game
        println!(
            "\n----\nTurns: {} Turn Score: {} Total Score: {}",
            turns,
            turn_score,
            total_score
        );

        match command_line("pig").as_ref() {

            // The player wants to roll the die
            "roll" | "r" => {
                // Get a die roll
                let roll = die_roll(seed_val as u64, 6);
                println!("Rolled {}", roll);

                // Increase the seed value
                seed_val += 1;

                // The game's "logic"; rolls of 1 throw out the current score
                if roll == 1 {
                    turn_score = 0;
                    turns += 1;
                } else {
                    // And rolls of anything else get folded into the turn score
                    turn_score += roll;
                };
            }

            // The player wants to save their current score
            "fold" | "f" => {
                total_score += turn_score;
                turn_score = 0;
                turns += 1;
            }

            // The player is done playing
            "quit" | "q" => { break; }

            // Something nonsensical was entered.
            other => { println!("I don't know what '{}' means.", other); }
        }
    }
    println!("You scored {} points!", total_score);
    Some(total_score)
}


/// Associates a player's score with their name.
struct Score {
    pub score: u64, 
    pub name: String,
}

/// Print out the scores in the order given.
fn report_scores(scores: &[Score]) {

    // Report at most the top 10 scores
    let len = if scores.len() > 10 {
        10
    } else { scores.len() };

    // Put a nice ASCII art pig first
    println!("           
           9
     ,--.-'-,--.
     \\  /-~-\\  /
    / )' a a `( \\   Leo Tindall
   ( (  ,---.  ) )
    \\ `(_o_o_)' /   A R C A D E   P I G
     \\   `-'   /
      | |---| |     for STDIO Jam 2017
      [_]   [_]                            ");
    println!("     +--------------------------+");
    println!("     |No. |          Name |Score|");
    println!("     +--------------------------+");


    // Look more impressive than a blank list if there are no scores
    if len == 0 {
        println!("     +--------------------------+");
        println!("     |    |               |     |");
        println!("     |   NO RECORDED  SCORES    |");
        println!("     |    |               |     |");
        println!("     +--------------------------+");
    }

    // Actually report the scores
    for line_number in 0..len {
        println!("     | {number:2} | {name:>width$} | {score:3} |",
                 number = line_number + 1,
                 score = scores[line_number].score,
                 width = 13,
		 name = scores[line_number].name,
                 );
        println!("     +--------------------------+");
    }
}

fn main() {

    // This records all previous scores
    let mut scores: Vec<Score> = Vec::new();


    // Run the game forever
    loop {
        clear_screen();
        report_scores(&scores);
	
	    println!("\n\n     +--------Press ENTER-------+");
	    command_line("");

        // Play a game with the player, and if the game is completed,
        // record the score.
        if let Some(score_value) = play() {
            scores.push(
                Score{
                    score: score_value,
                    name: command_line("Name"),
                }    
            );            

            // Sort the scores. sort_by takes a closure - essentially an anonymous
            // function - to which A (the current element) and B (the element being
            // compared) are passed. Here, rather than sorting A with B (which would
            // result in a lowest-to-highest order), B is sorted against A (to 
            // produce a highest-to-lowest order).
            scores.sort_by(|a, b| {b.score.cmp(&a.score)});
        }
    }
    
}
