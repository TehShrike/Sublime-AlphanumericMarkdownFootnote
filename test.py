from difflib import Differ
from FootnoteFunctions import insert_footnote, find_enclosing_footnote_id, find_footnote_marker_position, get_footnote_marker_id_at_position, get_footnote_body_position

def pretty_diff(actual, expected):
	lines = Differ().compare(
		actual.splitlines(keepends=True),
		expected.splitlines(keepends=True)
	)
	return ''.join(lines)

def assert_equal(actual, expected):
	if expected != actual:
		raise AssertionError(pretty_diff(actual, expected))

test_string = """
what's going on then[^ch1-1]

tell me all[^chb2] about it[^chc3]

[^ch1-1]: thingy

	stuff

   yeah

[^chb2]: meh?

	muh

wat

[^chc3]: whatever

"""

# def output(result):
# 	body = result['body']
# 	cursor = result['cursor']

# 	print(body[:cursor] + 'CURSOR' + body[cursor:])

# output(insert_footnote(test_string, 34))
# output(insert_footnote(test_string, 54))

# output(insert_footnote('what do you mean', 4))

# output(insert_footnote(test_string, 7))

assert_equal(find_enclosing_footnote_id(test_string, 66), None)
assert_equal(find_enclosing_footnote_id(test_string, 91), 'ch1-1')
assert_equal(find_enclosing_footnote_id(test_string, 100), 'ch1-1')
assert_equal(find_enclosing_footnote_id(test_string, 102), 'chb2')
assert_equal(find_enclosing_footnote_id(test_string, 103), 'chb2')
assert_equal(find_enclosing_footnote_id(test_string, 127), None)
assert_equal(find_enclosing_footnote_id(test_string, 136), 'chc3')

assert_equal(find_footnote_marker_position(test_string, 'nothing'), None)
assert_equal(find_footnote_marker_position(test_string, 'ch1-1'), 29)
assert_equal(find_footnote_marker_position(test_string, 'chb2'), 49)

assert_equal(get_footnote_marker_id_at_position(test_string, 21), None)
assert_equal(get_footnote_marker_id_at_position(test_string, 22), 'ch1-1')
assert_equal(get_footnote_marker_id_at_position(test_string, 23), 'ch1-1')
assert_equal(get_footnote_marker_id_at_position(test_string, 24), 'ch1-1')
assert_equal(get_footnote_marker_id_at_position(test_string, 29), 'ch1-1')
assert_equal(get_footnote_marker_id_at_position(test_string, 72), None)

assert_equal(get_footnote_body_position(test_string, 'ch1-1'), 76)
assert_equal(get_footnote_body_position(test_string, 'chb2'), 110)
assert_equal(get_footnote_body_position(test_string, 'wat'), None)


assert_equal(insert_footnote('what do you mean', 4)['body'], """what[^1] do you mean

[^1]: 

""")

assert_equal(insert_footnote(test_string, 7)['body'], """
what's[^ch1-1] going on then[^ch1-2]

tell me all[^chb3] about it[^chc4]

[^ch1-1]: 

[^ch1-2]: thingy

	stuff

   yeah

[^chb3]: meh?

	muh

wat

[^chc4]: whatever

""")

assert_equal(insert_footnote(test_string, 34)['body'], """
what's going on then[^ch1-1]

tel[^ch1-2]l me all[^chb3] about it[^chc4]

[^ch1-1]: thingy

	stuff

   yeah

[^ch1-2]: 

[^chb3]: meh?

	muh

wat

[^chc4]: whatever

""")

assert_equal(insert_footnote(test_string, 54)['body'], """
what's going on then[^ch1-1]

tell me all[^chb2] abou[^chb3]t it[^chc4]

[^ch1-1]: thingy

	stuff

   yeah

[^chb2]: meh?

	muh

[^chb3]: 

wat

[^chc4]: whatever

""")

test_string_2 = """
- find the previous footnote in the body
- pick a new number: the previous footnote's number, plus one
- find all footnotes greater to or equal than that number, and increment them in both the body and where the footnote contents are identified
- find the previous footnote's content block[^ch1-1]
- create a new footnote identifier where the cursor is[^ch1-2]
- create a new footnote contents block immediately after that content block
- move the cursor to the new footnote contents block

[^ch1-1]: yeah, footnote here


[^ch1-2]: aw yeah


"""

# output(insert_footnote(test_string_2, 11))

assert_equal(insert_footnote(test_string_2, 11)['body'], """
- find the[^ch1-1] previous footnote in the body
- pick a new number: the previous footnote's number, plus one
- find all footnotes greater to or equal than that number, and increment them in both the body and where the footnote contents are identified
- find the previous footnote's content block[^ch1-2]
- create a new footnote identifier where the cursor is[^ch1-3]
- create a new footnote contents block immediately after that content block
- move the cursor to the new footnote contents block

[^ch1-1]: 

[^ch1-2]: yeah, footnote here


[^ch1-3]: aw yeah


""")

test_string_with_unordered_footnotes = """
some text[^01-1]
some more text[^01-2]
hmmmm ok then[^01-3]

[^01-2]: original first

[^01-1]: original second

[^01-3]: original third
"""

assert_equal(insert_footnote(test_string_with_unordered_footnotes, 27)['body'], """
some text[^01-1]
some more[^01-2] text[^01-3]
hmmmm ok then[^01-4]

[^01-3]: original first

[^01-1]: original second

[^01-2]: 

[^01-4]: original third
""")


test_string_with_unordered_footnote_ids = """
some text[^01-3]
some more text[^01-1]
hmmmm ok then[^01-2]

[^01-2]: original first

[^01-1]: original second

[^01-3]: original third
"""

assert_equal(insert_footnote(test_string_with_unordered_footnote_ids, 45)['body'], """
some text[^01-4]
some more text[^01-1]
hmmmm[^01-2] ok then[^01-3]

[^01-3]: original first

[^01-1]: original second

[^01-2]: 

[^01-4]: original third
""")


test_string_with_unordered_footnote_ids_2 = """
some text[^01-3]
some more text[^01-1]
hmmmm ok then[^01-2]

[^01-3]: original first

[^01-1]: original second

[^01-2]: original third
"""

assert_equal(insert_footnote(test_string_with_unordered_footnote_ids_2, 45)['body'], """
some text[^01-4]
some more text[^01-1]
hmmmm[^01-2] ok then[^01-3]

[^01-4]: original first

[^01-1]: original second

[^01-2]: 

[^01-3]: original third
""")


















test_file = """
{pagebreak}





C> *…To the law and to the testimony!*
C> *If they do not speak according to this word,*
C> *it is because there is no light in them.*
C>
C> -- Genesis 1:28


{pagebreak}

# A summary of the debates on canon

## The thesis of this book - the Bible is self-authenticating

It is the thesis of this volume that the Bible should be the
axiomatic[^0-10] starting point and ending point for all Christian
doctrine,[^0-11] including the doctrine of canon.[^0-12] It will seek
to prove the Protestant doctrine that “only God can identify His
word,”[^0-13] and that He did so through the very prophets who gave us the Scriptures. In other words, if God's Word is the highest authority in our lives, there can be no higher authority to which we can appeal in order to prove the doctrine of canon. I will seek to prove that the Bible's self-referential statements are sufficient to completely settle the question of canonicity and that this presuppositional approach to canonicity is the only adequate approach that will stand up against all criticism. All other approaches to canonicity eviscerate the Bible of its ultimate authority.

## The Reformation position 

### The church has no authority to determine the canon

This has been the historic position of Protestantism. The Westminster Confession of Faith crystalizes the issue at stake when it states that the Bible is “the *only*
rule of faith and obedience.”[^0-14] Consistent Protestants have applied
this rigid criterion to the doctrine of canon as well as textual
criticism.[^0-15] This means that the Scriptures must be
self-authenticating in some way, not canonized by the church. This is
the fundamental difference between the Reformation Churches on the one
hand and both the Roman Catholic Church[^0-16] and the Eastern Orthodox
Church[^0-17] on the other hand. Rome and the Eastern Orthodox say that the
church determines the canon of Scripture and that the church has
authority over Scripture. But as J.I. Packer responded, 

> The church no more gave us the New Testament canon than Sir Isaac Newton gave us the force of gravity. God gave us gravity, by His work of creation, and
similarly He gave the New Testament canon, by inspiring the individual
books  that make it up.”[^0-18] 

There can be no higher authority by which Scripture is judged or the Scripture would cease to be the highest authority.

### The doctrine of canon must not contradict the doctrine of Sola Scriptura

The doctrine of *Sola Scriptura* is perhaps the most foundational doctrine of the Protestant Reformation, and as the Reformers themselves demonstrated, it was the most foundational teaching of the catholic (or universal) church of the first few centuries.[^0-1] *Sola Scriptura* is a Latin phrase that means "Scripture alone," and refers to the Reformation doctrine that the Bible is the *only infallible authority* for any area of life and that it is a *sufficient revelation* to know how to fully glorify God in every area of life - including how to recognize the canon. As Scripture words it, the Christian is called "not to think beyond what is written" in the Bible (1 Corinthians 4:6), and that the Bible gives us "all things that pertain to life and godliness" (2 Pet. 1:3) and is sufficient for doctrine, reproof, correction, instruction in righteousness and gives to us all other necessary information needed to make the man of God "complete, thoroughly equipped for every good work" (2 Tim. 3:15-17). After listing the sixty-six books of the Bible, the Westminster Confession of Faith stated the doctrine of Sola Scriptura this way:

> The whole counsel of God concerning all things necessary for his own glory, man's salvation, faith and life, is either expressly set down in Scripture, or by good and necessary consequence may be deduced from Scripture; unto which nothing at any time is to be added, whether by new revelations of the Spirit, or tradtions of men. (WCF I.6)

This statement claims that:

1.  The Bible contains *all the divine words needed* to know how to glorify God in every area of faith and life. 
2.  That nothing beyond the Bible (whether traditions of men or claims to new revelation from God) can be used to settle doctrine or to authoritatively show how to glorify God in faith and life. 
3.  That the use of logical deduction from the Scripture is not a violation of the previous two principles (since logic itself is imbedded in the Bible).

## Modern Protestant approaches to canon are inadequate

### Protestants have unwittingly abandoned sola Scriptura in their defence of Scripture

But while Protestants hold to this viewpoint theoretically, many are at
a loss about how to defend the Protestant canon of 66 books
presuppositionally.[^0-19] The moment they begin to appeal to evidence
that is outside the Bible to demonstrate that a book belongs in the
Bible, they are inconsistently acting as if there is a higher standard
by which that book can be judged. We Protestants believe that the 39
books of the Jewish Old Testament and the 27 books of the New Testament
are the only books that belong in the Bible. We reject the apocrypha and
claim that this official list of 66 Biblical books is our completed
“canon.”

But it is precisely at this point that Roman and Eastern Orthodox apologists insist that Protestants are inconsistent. Indeed, the modern Protestant failure to use Scripture alone to defend the canon of the Scripture is said to be the Achille's Heel[^0-2] of Protestantism. I have listened to dozens of debates between Roman Catholics and Protestants and I have sadly watched the Protestant leaders go down in flames. Why? Because they have inconsistently abandoned the Reformation principles of *Sola Scriptura* in their debate on canon. When Christians appeal to an authority outside of Scripture for canon, textual criticism, hermeneutics, ethics, church polity, etc., they have already lost the battle. It is my contention that Protestants need to return to the ancient doctrine of Sola Scriptura or they will be vulnerable to the apologetics of Romanists and/or the Eastern Orthodox.

The primary purpose of this book is to show how the first two summary statements on *Sola Scripture* (see above) can consistently be applied to the study of canon. Indeed, it is only as we do so that anyone can have an adequate basis for the topic of canon. But before we go there in the next section of this chapter, there are three foundational issues that Protestants must understand if they are to be effective.

### Protestants have often failed to see three necessary implications of Sola Scriptura

#### Logic is revealed in Holy Scripture 

It must be categorically asserted that the logical deductions[^0-3] that will be employed in this book ("good and necessary consequence" in the quote above) is also a consistent use of *Sola Scriptura.* 

Logic is embedded in the Scripture and cannot be avoided without avoiding the Scriptures themselves.[^0-4]  Scripture also assumes a prior logical understanding on the part of the readers.[^0-5]  In other words, it assumes that logic is part of man’s innate reasoning powers.  John Frame has shown how it is impossible to do theology, to apply Scripture to our lives, to understand the reasoning of Scripture, to communicate or even to have assurance of salvation apart from logic.[^0-6]  In several of his books, Gordon Clark has shown that this innate power to logically reason and discourse is the “image of God” in man.[^0-7]  It is not something alien that we impose on Scripture. Christ the Logos[^0-8] (John 1; 1 John 1:1) is the common Author of both since He not only gave Scripture, but also “gives light to every man who comes into the world” (John 1:9).  It is this innate grasp of logic that enables man (with effort) to perceive Scriptural argument just as the rules of language are innate and enable us (with effort) to perceive the grammatical forms of the text.[^0-9] It is true that the noetic affects of sin make us very prone to error in our use of logic.  But this just makes our study of logic that much more important if we are to grow in our understanding of ethics. 

To those who object that this approach to canonicity is engaged in circular reasoning, we
would make two observations: First, ultimate authority is always
circular by nature or it ceases to be the ultimate authority. As Hebrews
6:13 says, “For when God made a promise to Abraham, *because He could
swear by no one greater, He swore by Himself*.” God’s swearing by
Himself is a form of circularity, but it is an unavoidable
characteristic of any claim to ultimate authority. Second, to make an
argument for canon that implicitly makes the creature the ultimate
authority is not only self-defeating, but also irrational. It is
self-defeating in that it is seeking to prove that a canon of Scripture
is the ultimate authority while appealing to another source of authority
as more ultimate. It is irrational not only because of the inconsistency
of the previous point, but also because it jettisons the consistency of
a coherent “circle.” This is the difference between arguing in a
coherent circle and arguing in a vicious circle.[^0-20] Thus, to fully
appreciate the significance of this volume, it is helpful to study
Presuppositional Apologetics.[^0-21]

But even those who agree with the previous paragraphs might still be
puzzled about how we know which books are truly canonical. If
archaeologists found the “lost” letter mentioned in 1 Corinthians 5:9,
should it be included in the Bible? And if so, who would make that
determination? How do we know that Esther is part of Scripture? What
should we think about the Apocryphal books in the Roman Catholic Bible?
Is the canon closed? How do we know? How do we know that any of the
books of the Old and New Testaments are really Scripture?

Some Protestant theologians have felt the pressure of these questions and have
developed elaborate criteria by which to judge whether a book should be
included in the canon, but almost all of these criteria have come under
serious criticism.[^0-22] Are the criteria the same for the Old and New
Testaments? If not, why not? Who has the right to answer these
questions? Why were so many inspired books excluded from the canon of
Scripture during Old Testament times, even though these books were
clearly written by inspired contemporary prophets like Samuel (1 Sam.
10:25), Solomon (1Kings 4:32), and many others?[^0-23] Obviously inspiration is not the sole
criterion for canonicity, or many more books would have been included in
the canon.

But our application of sola Scriptura to the issue of canonicity should
not be taken as an individualistic decision. This is frequently the
charge brought against Protestants by both Roman Catholics and Eastern
Orthodox. However, the Reformers believed that to leave the judgment of
canonicity to each individual person would be both unbiblical and
self-destructive. For an individual to determine what he thinks is (or
is not) Scripture would be to place man as a judge of Scripture and
ultimately as a judge of God. Though Luther was troubled by the book of
James, he seemed to recognize that his personal opinions could not be
the criteria for what is or is not canonical.

On the other hand, if the decision is a corporate decision, we need to
ask the question, “Which group gets to decide?” The Samaritans and Sadducees)[^0-24] only accepted the first five books of the
Old Testament. The Alexandrian Jews may have added some apocryphal
books,[^0-25] while the Essenes may have added some and excluded others.[^0-26] The Pharisees accepted the same books that the
Protestants now accept, but what makes their view authoritative? Even if we agreed
with the Pharisees because the vast majority of Jews did so, what would
make them right and others wrong? Surely there must be a more
authoritative standard than an appeal to the very Pharisees whom Christ
opposed!

## Roman Catholic and Eastern Orthodox approaches inadequate

[^0-1]: Calvin, Luther, Mornay, and many other Reformers demonstrated that 
    Rome had abandoned the catholic faith on this any many other doctrines. When I deal with Roman Catholic and Eastern Orthodox objections to the Reformation view of the canon later in this book, I will document the pervasive belief in the doctrine of Sola Scriptura in the church of the first millennium. Cyril of Jerusalem (AD 313-386) is representative of many when he says, 

    > For concerning the divine and sacred Mysteries of the Faith, we ought not to deliver even the most casual remark without the Holy Scriptures: nor be drawn aside by mere probabilities and the artifices of argument. Do not then believe me because I tell thee these things, unless thou receive from the Holy Scriptures the proof of what is set forth: for this salvation, which is of our faith, is not by ingenious reasonings, but by proof from the Holy Scriptures. 

[^0-2]: According to ancient Greek legend, the great warrior, Achilles, had 
    been dipped in magical waters as a baby that would make him invulnerable to attack. Since Achilles was held by the heel, the heel was not immersed, and therefore the heel alone was vulnerable to wounds. That one weakness would be exploited near the end of the Trojan War by Paris. As the story goes, he shot Achilles in the heel with an arrow, killing his seemingly invincible foe. Thus, to have an "Achilles heel" is a metaphor of having a weak point in our defenses. Many Roman Catholic apologists claim that sola Scriptura is not Protestantism's greatest strength, but its greatest weakness. 

[^0-3]: What the Confession calls "good and necessary consequence" (Westminster Confession of Faith, I.6)

[^0-4]: Just as J.C. Keister, “Math and the Bible,” in The Trinity Review  
    (No. 27/Sept/Oct, 1992) has shown the axioms of mathematics to be embedded in the Scripture, John Robbins and others have demonstrated that all the axioms of logic are used in Scripture and thus show the divine warrant for a complete system of logic.  Some might ask, “Which system of logic?”  Actually there are not truly different systems of logic.  Gordon Clark has shown that there is a problem with Bertrand Russell’s modification of Aristotelian logic, and cautions against it,  However, the basic structure of logical thinking cannot be different.  For proof of where Russell went wrong, see Clark's book, *Logic*, pp. 83ff.  For a marvelous college level course on logic using the Bible as the source, write to the Trinity Foundation in Jefferson, MD.

[^0-5]: 
    {#chapter-1-footnote-4}
    Let me quote at length from John Frame, The Doctrine of The Knowledge 
    of God (Phillipsburg, NJ: Presbyterian & Reformed Publishing Company, 1987), pp. 251-254.
    
    > One may not, however, do theology or anything else in human life without taking account of those truths that form the basis of the science of logic.  We cannot do theology if we are going to feel free to contradict ourselves or to reject the implications of what we say.  Anything that we say must observe the law of noncontradiction in the sense that it must say what it says and not the opposite…
    >
    > When we see what logic is, we can see that it is involved in many biblical teachings and injunctions.  (i) It is involved in any communication of the Word of God.  To communicate the Word is to communicate the Word as opposed to what contradicts it (1 Tim. 1:3ff; 2 Tim. 4:2f.).  Thus the biblical concepts of wisdom, teaching, preaching, and discernment presuppose the law of non-contradiction.
    >
    > (ii) It is involved in any proper response to the Word.  To the extent that we don’t know the implications of Scripture, we do not understand the meaning of Scripture.  To the extent that we disobey the applications of Scripture, we disobey Scripture itself.  God told Adam not to eat the forbidden fruit.  Imagine Adam replying, “Lord, you told me not to eat it, but you didn’t tell me not to chew and swallow!”  God would certainly have replied that Adam had the logical skill to deduce “You shall not chew and swallow” from “You shall not eat.”  In such a way, the biblical concepts of understanding, obeying, and loving presuppose the necessity of logic.
    >
    > (iii) Logic is involved in the important matter of assurance of salvation.  Scripture teaches that we may know that we have eternal life (1 John 5:13).  The Spirit’s witness (Rom 8:16ff.) plays a major role in this assurance; but that witness does not come as a new revelation, supplementing the canon, as it were.  So where does the information that I am a child of God come from - information to which the Spirit bears witness?  It comes from the only possible authoritative source, the canonical Scriptures.  But how can that be, since my name is not found in the biblical text?  It comes by application of Scripture, a process that involves logic.  God says that whosoever believes in Christ shall be saved (John 3:16).  I believe in Christ.  Therefore I am saved.  Saved by a syllogism?  Well, in a sense, yes.  If that syllogism were not sound, we would be without hope.  (Of course, the syllogism is only God’s means of telling us the good news!)  Without logic, then, there is no assurance of salvation.
    >
    > (iv) Scripture warrants many specific types of logical argument.  The Pauline Epistles, for instance, are full of “therefores.”  Therefore indicates a logical conclusion.  In Romans 12:1 Paul beseeches us, “Therefore, by the mercies of God.”  The mercies of God are the saving mercies that Paul has described in Romans 1-11.  Those mercies furnish us with grounds, reasons, premises for the kind of behavior described in chapters 12-16.  Notice that Paul is not merely telling us in Romans 12 to behave in a certain way.  He is telling us to behave in that way for particular reasons.  If we claim to obey but reject those particular reasons for obeying, we are to that extent being disobedient.  Therefore Paul is requiring our acceptance not only of a pattern of behavior but also of a particular logical argument.  The same thing happens whenever a biblical writer presents grounds for what he says.  Not only his conclusion but also his logic is normative for us.  If, then, we reject the use of logical reasoning in theology, we are disobeying Scripture itself…
    >
    > (v) Scripture teaches that God himself is logical.  In the first place, His Word is truth (John 17:17), and truth means nothing if it is not opposed to falsehood.  Therefore His Word is noncontradictory.  Furthermore, God does not break His promises (2 Cor. 1:20); He does not deny himself (2 Tim. 2:13); He does not lie (Heb. 6:18; Tit. 1:2).  At the very least, those expressions mean that God does not do, say, or believe the contradictory of what He says to us.  The same conclusion follows from the biblical teaching concerning the holiness of God.  Holiness means that there is nothing in God that contradicts His perfection (including His truth).  Does God, then, observe the law of noncontradiction?  Not in the sense that this law is somehow higher than God himself.  Rather, God is himself noncontradictory and is therefore himself the criterion of logical consistency and implication.  Logic is an attribute of God, as are justice, mercy, wisdom, knowledge.  As such, God is a model for us.  We, as His image, are to imitate His truth, His promise keeping.  Thus we too are to be noncontradictory.
    >
    > Therefore the Westminster Confession of Faith is correct when it says (l, vi) that the whole counsel of God is found not only in what Scripture explicitly teaches but also among those things that “by good and necessary consequence may be deduced from Scripture.”  This statement has been attacked even by professing disciples of Calvin, but it is quite unavoidable.  If we deny the implications of Scripture, we are denying Scripture…
    >
    > I would therefore recommend that theological students study logic, just as they study other tools of exegesis.  There is great need of logical thinking among ministers and theologians today.  Invalid and unsound arguments abound in sermons and theological literature.  It often seems to me that standards of logical cogency are much lower today in theology than in any other discipline.  And logic is not a difficult subject.  Anyone with a high school diploma and some elementary knowledge of mathematics can buy or borrow a text like I.M. Copi, Introduction to Logic and go through it on his own…

[^0-6]: See discussion in [previous footnote](#chapter-1-footnote-4).

[^0-7]: See for example Gordon Clark’s discussion in A Christian Philosophy of 
    Education (Jefferson, MD: The Trinity Foundation, 1988), pp. 129-140.

[^0-8]: Which has in its meaning both logic and discourse.  Christ is the Word 
    of God.  He is also the Logic of God.

[^0-9]: This of course does not mean that we do not need to study language.  
    But linguistic analysis has demonstrated that children from every language group use the same “rules” to make sense out of the patterns of words that they hear.  There is something innate (God-given) that enables them to learn a language.  See Gordan Clark, Religion, Reason and Revelation.  In the same way, God’s people must study logic to improve their understanding of Scripture, but 

[^0-10]: The New Testament word for "presuppositions" is στοιχεια. This
    word was used in classical Greek and by the Church fathers to mean
    the elementary or fundamental principles. In Geometry it was used
    for axioms, and in philosophy for elements of proof or the πρωτοι
    συλλογισμοῖ of general reasoning (Liddell and Scott, *A
    Greek-English Lexicon, s.v.* ). Obviously both of these definitions
    are synonyms with "presuppositions." 

    The New Testament teaches that
    the στοιχεια are the "foundation" upon which our faith and practice
    rests (Heb. 5:12-6:3). We find our στοιχεια in the Word of God (Heb.
    5:12) and most specifically in the person of Jesus Christ (Col.
    2:8-10; Heb. 6:1) revealed in them. The στοιχεια of the world are
    the foundation of the non-Christian "philosophy" (Col. 2:8) and are
    diametrically opposed to the στοιχεια of Christ the God-Man (Col
    2:8-10). Our thoughts and actions are a logical outworking of these
    στοιχεια in everyday life (Col. 2:20ff). We must recognize that the
    superstructure of our world-and-life view is antithetical to the
    superstructure of the heathen's world-and-life view, not because the
    superstructures do not have any things in common, but because of the
    way in which these superstructures are completely committed to their
    foundation or presuppositions. Paul gives us an example of this
    concept when he vigorously opposed the Galatians’ succumbing to
    pressure to be circumcised and observe "days and months and times
    and years" (Gal. 4:10). Though the physical act of circumcision was
    not wrong (cf. 1 Cor. 7:19; Acts 16:3), the *idea* that lay behind
    it was destructive and led to syncretism, a denial of their
    presuppositions and an unintentional reversion to weak and pathetic
    presuppositions (Gal. 4:9). 

    The study of canon is not a neutral
    subject. It either flows from a faithful commitment to the Bible’s
    total authority or it of necessity substitutes another competing
    authority (such as Tradition, Councils, Pope, Koran, imam, personal
    opinion, etc) with disastrous consequences.

[^0-11]: As the Westminster Confession of Faith words it, “The infallible
    rule of interpretation of Scripture is the Scripture itself; and
    therefore, when there is a question about the true and full sense of
    any Scripture (which is not manifold, but one), it must be searched
    and known by other places that speak more clearly.” The supreme
    judge by which all controversies of religion are to be determined,
    and all decrees of councils, opinions of ancient writers, doctrines
    of men, and private spirits, are to be examined, and in whose
    sentence we are to rest, can be no other but the Holy Spirit
    speaking in the Scripture.” (WCF I.ix-x). As we will see, this is
    just as true of the doctrine of canonicity as it is any other
    doctrine.

[^0-12]: “Canon” is a term that refers either 1) to a rule of faith and
    truth or 2) to the list of books which are considered to be part of
    Holy Scripture. In this book I will be using the latter definition.
    The canon of Scripture is the authoritative list of books that are
    considered to be Scripture. The Westminster Confession of Faith
    insists that God alone can determine canon. Otherwise man is the
    judge of God’s revelation. While there are many circumstantial
    evidences that God has orchestrated, “our full persuasion and
    assurance of the infallible truth and divine authority thereof, is
    from the inward work of the Holy Spirit bearing witness by and with
    the Word in our hearts” (I.v). It is *God* who determines the canon
    of Scripture.

[^0-13]: Greg L. Bahnsen, “The Concept and Importance of Canonicity,” an
    unpublished paper given to the author by Greg. L. Bahnsen. This
    seminal paper triggered a desire in me to be totally consistent with
    my presuppositional starting point of Scripture. Bahnsen has also
    applied this presuppositional approach to the question of whether
    the Bible is inerrant in, Greg. L. Bahnsen, “Inductivism, Inerrancy,
    and Presuppositionalism,” in *The Journal of the Evangelical
    Theological Society,* volume 20, 1997. This is a brilliant response
    to opponents of inerrancy.

[^0-14]: Westminster Larger Catechism \#3, emphasis mine.

[^0-15]: For a presuppositional approach to textual criticism, see my book,
    *“Has God Indeed Said?: The Preservation of the Text of Scripture,*
    available for free download from <http://biblicalblueprints.org/>.

[^0-16]: Karl Keating represents Roman Catholicism when he says that “an
    infallible authority is needed if we are to know what belongs in the
    Bible and what does not. Without such an authority, we are left to
    our own prejudices, and we cannot tell if our prejudices lead us in
    the right direction… \[The authority needed is\] an infallible,
    teaching Church… The same Church that authenticates the Bible, that
    establishes inspiration, is the authority set up by Christ to
    interpret his word.” Karl Keating, *Catholicism and Fundamentalism*
    (San Francisco: Ignatius Press, 1988), pp. 132,133.

[^0-17]: Bishop Kallistos (Timothy Ware) states the Eastern Orthodoxy
    position this way: “It is from the Church that the Bible ultimately
    derives its authority, for it was the Church which originally
    decided which books form a part of Holy Scripture.” Timothy Ware,
    *The Orthodox Church* (New York: Penguin Books, 1997), p. 199.

[^0-18]: James Packer, *God Speaks to Man: Revelation and the Bible,*
    Christian Foundations, 6 (Philadelphia: Westminster Press, 1965),
    p.81

[^0-19]: For example, conservative scholar, Roland Kenneth Harrison, in
    his excellent book, *Introduction to the Old Testament,* wrongly
    states, “While the Bible legitimately ought to be allowed to define
    and describe canonicity, it has in point of fact almost nothing to
    say about the manner in which holy writings were assembled, or the
    personages who exercised an influence over the corpus during the
    diverse stages of its growth.” See Roland Kenneth Harrison,
    *Introduction to the Old Testament* (Grand Rapids: Eerdmans, 1969),
    p. 262. 

    He says this despite the fact that he agrees with the
    Protestant principle that the Scriptures are “self-authenticating”
    and “do not derive their authority either from individual human
    beings or from corporate ecclesiastical pronouncements” (p. 263). He
    rightly rejects the Roman Catholic assumption that the church is the
    “mother of the Bible” and has authority to determine the canon by
    asserting that “\[h\]istorical investigation is no more fruitful in
    uncovering significant information about the activities of synods or
    other authoritative bodies with regard to the formation of the Old
    Testament canon than any other form of study” (p. 262).

    But his
    position is weak, leaving us with a presupposition about the
    self-authenticating nature of the Scriptures, but a failure to pull
    that presupposition from the Scripture itself. It is the intent of
    this book to show that the Bible is full of information speaking to
    the issue of canonicity.

[^0-20]: Greg L. Bahnsen says, “The ‘circularity’ of a transcendental
    argument is not at all the same as the fallacious ‘circularity’ of
    an argument in which the conclusion is a restatement (in one form or
    another) of one of its premises. Rather, it is the circularity
    involved in a coherent theory (where all the parts are consistent
    with or assume each other) and which is required when one reasons
    about a precondition for reasoning. Because autonomous philosophy
    does not provide the preconditions for rationality or reasoning, its
    ‘circles’ are destructive of human thought – i.e., ‘vicious’ and
    futile endeavors.” Greg Bahnsen, *Van Til's Apologetics: Readings
    and Analysis* (Phillipsburg, Presbyterian and Reformed, 1998), 518.

[^0-21]: There are two forms of Presuppositional Apologetics that (while
    competing with each other) have both offered very helpful insights
    about the nature of presuppositional reasoning. An excellent
    introduction to Van Tillian apologetics can be found in Greg L.
    Bahnsen, *Always Ready: Directions for Defending the Faith*
    (Texarkana, AR: Covenant Media Foundation, 1996). The second form of
    presuppositionalism can be found in the brilliant writings of Gordon
    H. Clark. An excellent and brief introduction to Clarkianism can be
    found in Gary W. Crampton, *The Scripturalism of Gordon H. Clark*
    (Jefferson, MD: Trinity Foundation, 1999). This book contains a
    comprehensive bibliography of all of Dr. Clark’s writings.

[^0-22]: For example, if the “antiquity” rule is correct, how could people
    have accepted the writings of Moses the moment they were written? No
    book of the Bible met the “antiquity” rule for the first people who
    used those books as Scripture. Furthermore, this rule assumes
    without proof the closing of the canon. If the “apostle” rule is
    used for the New Testament Scriptures, then what do we do about the
    books not written by apostles (Mark, Luke, Acts, Hebrews, James, and
    Jude)? 

    It seems rather
    arbitrary to say that they were written under the general oversight
    of apostles. (Mark is said to be written under Petrine authority and
    Luke-Acts is said to be written under Pauline authority. Supposedly,
    once the non-apostles wrote the books, the apostles read them and
    gave their stamp of approval upon them.). But the problem is that no
    apostle was inspired to write these books. They were the direct
    revelation of God to New Testament prophets. We will look at this
    issue in more detail later in the book. Almost every man-made
    criterion for evaluating canon has come under criticism. While some
    of the criteria have validity (for example, agreement with the
    Torah, unity and self-testimony, preservation, etc), it is the
    purpose of this book to show that the Scripture has given us
    everything that we need to determine the canon of the Old and New
    Testaments. 

    One rule that will be used in the second half of this book is the Biblical
    doctrine of inerrancy. But this rule will primarily be used in an ad
    hominem way. We will introduce a few other Biblical rules by
    which other literature (such as the Koran) can be judged. But the first half of this book will restrict its discussion to the Biblical proofs for the Protestant canon. Note: Though many people believe that Paul wrote Hebrews, there is abundant evidence that Luke wrote Hebrews. For an introduction to this subject, see David L. Allen, *Lukan Authorship of Hebrews,* (Nashville: B&H Publishing, 2010). 

[^0-23]: See for example, the Book of The Wars of Jehovah (Numb. 21:14),
    the Book of Jashar (Josh 10:13; 2 Sam. 1:18), another Book of Samuel
    on the Kingdom (1 Sam. 10:25), the Book of the Chronicles of David
    (1Chron. 27:24), the Book of the Acts of Solomon (1Kings 11:41),
    Solomon’s three thousand proverbs and 1005 songs (1Kings 4:32), the
    book of Solomon’s Natural History (1Kings 4:32,33), the Book of Shemaiah the Prophet (2Chron. 12:15), the prophecy of Ahijah the Shilonite (2Chron. 9:29), the Visions of Iddo the seer (2Chron. 9:29; 12:15), “the annals of the prophet Iddo”
    (2Chron. 13:22), a full history of king Uzziah written by Isaiah
    (2Chron. 26:22), the Book of Jehu the Son of Hanani (2Chron. 20:34),
    and an extrabiblical (but reliable) history of the Kings (1Kings
    14:19,25; Chron. 20:34; 33:18).

[^0-24]: Though this is contested by some scholars, I believe the evidence 
    favors the view that the Saduccees did not accept any books as authoritative beyond the Pentateuch. Since they were literalists in their interpretation, it is almost certain that they would have believed in the resurrection and in spirits (contra Matt. 22:23; Acts 23:8) if they took the rest of the Old Testament as authoritative.

    Likewise, it seems unlikely that Christ would have appealed to such an obscure passage in the Pentateuch when arguing with them (Matt. 22:32 quotes Ex. 3:6), if the Sadducees had been willing to accept the authority of much more obvious texts on the resurrection, such as Isaiah 26:19; Job 19:25-26; Dan. 12:2; etc. Hippolytus of Rome (170-235 AD) said that the Sadducees "do not, however, devote attention to prophets, but neither do they to any other sages, except to the law of Moses only…" Origen also claimed that "the Samaritans and Sadducees… receive the books of Moses alone." But I do grant that some scholars have concluded differently. For example, F.F. Bruce states,

    > It is probable, indeed, that by the beginning of the Christian era the Essenes (including the Qumran community) were in substantial agreement with the Pharisees and the Sadducees about the limits of the Hebrew scripture.

    F.F. Bruce, The Canon of Scripture (Downers Grove: InterVarsity, 1988), p. 40. 

[^0-25]: Though this conclusion is not shared by scholars such as F.F. Bruce, 
    who says,

    > Philo of Alexandria (c 20 BC-AD 50) evidently knew the scriptures in the Greek version only. He was an illustrious representative of Alexandrian Judaism, and if Alexandrian Judaism did indeed recognize a more comprehensive canon than Palestinian Judaism, one might have expected to find some trace of this in Philo's voluminous writings. But, in fact, while Philo has not given us a formal statement on the limits of the canon such as we have in Josephus, the books which he acknowledged as holy scripture were quite certainly books included in the traditional Hebrew Bible… he shows no sign of accepting the authority of any of the books which we know as the Apocrypha. 

    (Bruce, The Canon of the Scripture, pp. 29-30) 

    Beckwith says, 

    > It is difficult to conceive of the canon being organized according to a rational principle, or of its books being arranged in a definite order, unless the identity of those books was already settled and the canon closed, still more is it difficult to conceive of those books being counted, and the number being generally accepted and well known, if the canon remained open and the identity of its books uncertain. Even if there were not (as in fact there is) evidence to show which books it was that were counted, sometimes alphabetically as 22, sometimes more simply as 24, the presumption would still hold good that the identity of the books must have been decided before they could be counted, and that agreement about their number implies agreement about their identity. And such agreement, as we have now seen, had probably been reached by the second century BC.

    Roger Beckwith, The Old Testament Canon of the New Testament Church (Grand Rapids: Eerdmans, 1985), pp. 262-263.

[^0-26]: This too has been disputed by many. See chapters referenced in 
    previous footnotes from F.F. Bruce and Roger Beckwith. 

[^0-27]: Under our discussion of “tradition” we will examine the
    Protestant approach to the church being the pillar and ground of the
    truth. It has no reference to an infallible tradition or an
    infallible church. Rather it is the mandate that the church
    faithfully preserve the teachings of the Scripture that have been
    given to it by the apostles: “These things I write to you…” (v. 4);
    “I write to you so that…” (v. 5). 

    The church has failed to be the
    pillar and ground of the truth when it fails to derive 100% of its
    teachings from the Bible. As Paul elsewhere stated, “that you may
    learn in us not to think beyond what is written” (1Cor. 4:6). But
    this phrase, “the pillar and ground of the truth,” does help to
    correct the misguided view of solo Scriptura that is advocated by
    some Protestants. Sola Scriptura takes seriously God’s providential
    work through the church to preserve His doctrines. Solo Scriptura is
    so radically individualistic that it wants each individual to
    reinvent the wheel, and fails to honour the teachers that God has
    given to the church.

[^0-28]: In 1546 (at the Council of Trent) Rome officially added the
    following books (or portions of books) to the canon: Tobit, Judith,
    the Greek additions to Esther, the Wisdom of Solomon, Sirach,
    Baruch, the Letter of Jeremiah, three Greek additions to Daniel (the
    Prayer of Azariah and the Song of the Three Jews, Susanna, and Bel
    and the Dragon), and I and 2 Maccabees.

[^0-29]: The Greek Orthodox Church added 1 Esdras, the Prayer of Manasseh,
    Psalm 151, and 3 Maccabees to the books accepted by the Roman
    Catholic Church.

[^0-30]: The Slavonic (Russian) Orthodox Church adds to the Greek Orthodox
    canon the book of 2 Esdras, but designates I and 2 Esdras as 2 and 3
    Esdras.

[^0-31]: The Coptic Church adds the two Epistles of Clement to the
    Protestant canon.

[^0-32]: The Ethiopian Orthodox Church has the largest canon of all. To
    the apocryphal books found in the Septuagint Old Testament, it adds
    the following: Jubilees, I Enoch, and Joseph ben Gorion’s
    (Josippon’s) medieval history of the Jews and nations. To the 27
    books of the New Testament they add eight additional texts: namely
    four sections of church order from a compilation called Sinodos, two
    sections from the Ethiopic Book of the Covenant, Ethiopic Clement,
    and Ethiopic Didascalia. It should be noted that for the New
    Testament they have a broader and a narrower canon. The narrower
    canon is identical to the Protestant and Catholic canon.

[^0-33]: The Armenian Bible includes the History of Joseph and Asenath and
    the Testaments of the Twelve Patriarchs, and the New Testament
    included the Epistle of Corinthians to Paul and a Third Epistle of
    Paul to the Corinthians

[^0-34]: Some Orthodox churches add the book of 4 Maccabees as well.

[^0-35]: Pope Gregory the Great said, "We shall not act rashly, if we accept a testimony of books, which, although not canonical, have been published for the edification of the Church." Moral Treatises 19.21, citing a passage from Maccabees. 

[^0-36]: The Prologue to the Glossa ordinaria (1498 AD), states,

    > Many people, who do not give much attention to the holy scriptures, think that all the books contained in the Bible should be honored and adored with equal veneration, not knowing how to distinguish among the canonical and non-canonical books, the latter of which the Jews number among the apocrypha. Therefore they often appear ridiculous before the learned; and they are disturbed and scandalized when they hear that someone does not honor something read in the Bible with equal veneration as all the rest. Here, then, we distinguish and number distinctly first the canonical books and then the non-canonical, among which we further distinguish between the certain and the doubtful.
    >
    > The canonical books have been brought about through the dictation of the Holy Spirit. It is not known, however, at which time or by which authors the non-canonical or apocryphal books were produced. Since, nevertheless, they are very good and useful, and nothing is found in them which contradicts the canonical books, the church reads them and permits them to be read by the faithful for devotion and edification. Their authority, however, is not considered adequate for proving those things which come into doubt or contention, or for confirming the authority of ecclesiastical dogma, as blessed Jerome states in his prologue to Judith and to the books of Solomon. But the canonical books are of such authority that whatever is contained therein is held to be true firmly and indisputably, and likewise that which is clearly demonstrated from them. For just as in philosophy a truth is known through reduction to self-evident first principles, so too, in the writings handed down from holy teachers, the truth is known, as far as those things that must be held by faith, through reduction to the canonical scriptures that have been produced by divine revelation, which can contain nothing false. Hence, concerning them Augustine says to Jerome: To those writers alone who are called canonical I have learned to offer this reverence and honor: I hold most firmly that none of them has made an error in writing. Thus if I encounter something in them which seems contrary to the truth, I simply think that the manuscript is incorrect, or I wonder whether the translator has discovered what the word means, or whether I have understood it at all. But I read other writers in this way: however much they abound in sanctity or teaching, I do not consider what they say true because they have judged it so, but rather because they have been able to convince me from those canonical authors, or from probable arguments, that it agrees with the truth.

    Translation by Dr. Michael Woodward from the following latin:

    > Quoniam plerique eo quod non multam operam dant sacrae Scripturae, existimant omnes libros qui in Bibliis continentur, pari veneratione esse reverendos atque adorandos, nescientes distinguere inter libros canonicos, et non canonicos, quos Hebraei a canone separant, et Graeci inter apocrypha computant; unde saepe coram doctis ridiculi videntur, et perturbantur, scandalizanturque cum audiunt aliquem non pari cum caeteris omnibus veneratione prosequi aliquid quod in Bibliis legatur: idcirco hic distinximus, et distincte numeravimus primo libros canonicos, et postea non canonicos, inter quos tantum distat quantum inter certum et dubium. Nam canonici sunt confecti Spiritus sancto dictante non canonici autem sive apocryphi, nescitur quo tempore quibusve auctoribus autoribus sint editi; quia tamen valde boni et utiles sunt, nihilque in eis quod canonicis obviet, invenitur, ideo Ecclesia eos legit, et permittit, ut ad devotionem, et ad morum informationem a fidelibus legantur. Eorum tamen auctoritas ad probandum ea quae veniunt in dubium, aut in contentionem, et ad confirmandam ecclesiasticorum dogmatum auctoritatem, non reputatur idonea, ut ait beatus Hieronymus in prologis super Judith et super libris Salomonis. At libri canonici tantae sunt auctoritatis, ut quidquid ibi continetur, verum teneat firmiter et indiscusse: et per consequens illud quod ex hoc concluditur manifeste; nam sicut in philosophia veritas cognoscitur per reductionem ad prima principia per se nota: ita et in Scripturis a sanctis doctoribus traditis veritas cognoscitur, quantum ad ea quae sunt fide tenenda, per reductionem ad Scripturas canonicas, quae sunt habita divina revelatione cui nullo modo potest falsum subesse. Unde de his dicit Augustinus ad Hieronymum: Ego solis eis scriptoribus qui canonici appellantur, didici hunc timorem honoremque deferre, ut nullum eorum scribendo errasse firmissime teneam; ac si aliquid in eis offendero quod videatur contrarium veritati, nihil aliud existimem quam mendosum esse codicem, vel non esse assecutum interpretem quod dictum est, vel me minime intellexisse, non ambigam. Alios autem ita lego, ut quantalibet sanctitate doctrinave polleant, non ideo verum putem quia ipsi ita senserunt, sed quia mihi per illos auctores canonicos vel probabiles rationes, quod a vero non abhorreat, persuadere potuerunt 

    Biblia cum glosa ordinaria et expositione Lyre litterali et morali (Basel: Petri & Froben, 1498), British Museum IB.37895, Vol. 1, On the canonical and non-canonical books of the Bible. Translation by Dr. Michael Woodward.

[^0-37]: The following is a brief list of famous churchmen who clearly stood 
    against Rome's views on the apocrypha: Melito of Sardis (died 180 AD), Origen (184-254), Athanasius (296-373), Cyril of Jerusalem (313-386), Gregory of Nazianzus (329-390), Hilary of Poitiers (310-367), Epiphanius, Basil the Great (330-379), Jerome (347-420), Rufinus, Primasius (died 560), Gregory the Great (590-604), The Venerable Bede (673-735), Agobard of Lyons (779-840), Alcuin (735-804), Walafrid Strabo (808-849), Haymo of Halberstadt (died 853), Ambrose of Autpert (730-784), Radulphos Flavicencius (1063-122), Hugh of St. Victor (1096-1141), Richard of St. Victor (died 1155), John of Salisbury (1120-1180), Peter Cellensis (1115-1183), Rupert of Deutz (1075-1129), Honorius of Autun (1080-1154), Peter Comestor (died 1178), Peter Maritius or Peter the Venerable (1092-1156), Adam Scotus (1140-1212), Hugo of St. Cher (1200-1263), Philip of Harveng (died 1183), Nicholas of Lyra (1270-1340), William of Ockham (1287-1347), Antoninus (died 1459), Alanso Tostado (1414-1455), Dionysius the Carthusian (1402-1471), Thomas Walden (1375-1430), Jean Driedo (condemned Luther's teachings in 1519), John Ferus, and Jacobus Faber Stapulensis (1455-1536) could all be cited as contradicting Trent's claim to represent tradition on the apocrypha.

    Rome appeals to the local councils of Hippo (393) and Carthage (397) as proof that the apocrypha were accepted by the early church, but those councils prove too much since they included books that both Rome and the Eastern Orthodox church reject as canonical. It is better to take Cajetun's interpretations of those councils (see next footnote), and treat them as having two levels of canon - a church canon of books acceptable to read, and God's canon of books that are inspired and part of Scripture. 

[^0-38]: Fascinatingly, Cardinal Cajetan explained that the historical church 
    used the term canonical to refer to two different categories of books: books useful to be read in church, but not part of Scripture, and books that are part of Scripture. He said,

    > Here we close our commentaries on the historical books of the Old Testament. For the rest (that is, Judith, Tobit, and the books of Maccabees) are counted by St Jerome out of the canonical books, and are placed amongst the Apocrypha, along with Wisdom and Ecclesiasticus, as is plain from the Prologus Galeatus. Nor be thou disturbed, like a raw scholar, if thou shouldest find anywhere, either in the sacred councils or the sacred doctors, these books reckoned as canonical. For the words as well of councils as of doctors are to be reduced to the correction of Jerome. Now, according to his judgment, in the epistle to the bishops Chromatius and Heliodorus, these books (and any other like books in the canon of the bible) are not canonical, that is, not in the nature of a rule for confirming matters of faith. Yet, they may be called canonical, that is, in the nature of a rule for the edification of the faithful, as being received and authorised in the canon of the bible for that purpose. By the help of this distinction thou mayest see thy way clearly through that which Augustine says, and what is written in the provincial council of Carthage.

    In ult. Cap. Esther. Taken from A Disputation on Holy Scripture by William Whitaker (Cambridge: University, 1849), p. 48. See also Cosin's A Scholastic History of the Canon, Volume III, Chapter XVII, pp. 257-258 and B.F. Westcott's A General Survey of the Canon of the New Testament, p. 475.

[^0-39]: Metzger, Bruce M. (March 13, 1997). The Canon of the New Testament: 
    Its Origin, Development, and Significance. Oxford University Press. p. 246. "Finally on 8 April 1546, by a vote of 24 to 15, with 16 abstensions, the Council issued a decree (De Canonicis Scripturis) in which, for the first time in the history of the Church, the question of the contents of the Bible was made an absolute article of faith and confirmed by an anathema."

[^0-40]: In a later chapter we will see that while there were numerous church 
    fathers from the second through fourth centuries who endorsed the shorter Protestant canon, and while while even Jerome (the translator of the Latin Vulgate used by Rome) agrees book-for-book with the Protestant canon, there is no document during the same period that matches the canon of Trent book-for-book. Roman apologists continually appeal to the late fourth-century councils of Hippo and Carthage as including some apocryphal books, but those two councils only list 43 of the 46 books of Trent. They omit Lamentations and Baruch and mention five books of Solomon (which Trent excludes). Those councils were not ecumenical councils, but local, and as Cajetun mentions, used the term "canon" in two senses - a church canon of books approved for reading and God's canon of books inspired and part of Scripture.

[^0-41]: We will have much more to say about the Roman Catholic view of canon 
    in a later chapter.

[^0-42]: The following chart shows division of opinion on which apocryphal 
    books were sufficiently beneficial as to include for the edification of the church. The fact that the following apocryphal books were included in various editions of their Bibles no more proves that they were treated as Scripture than the Protestant Bibles with the apocrypha proves that Protestants believed they were Biblical. Nevertheless, for purposes of argument, notice the variations of which apocryphal books were included:

    | Books           | Greek   | Slav   | Geor   | Arme   | Syri   | Ethi   | Assy   |
    | --------------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
    | 1Esdras         | Y       | Y       | Y       | N       | N       | Y       | N       |
    | 2Esd. 13-14     | N       | N       | Y       | N       | N?      | Y       | N?      |
    | 5&6Ezra         | N       | N       | N       | N       | N       | N       | N       |
    | 3Maccabees      | Y       | Y       | Y       | N       | Y       | N       | Y       |
    | 4Maccabees      | N       | N       | Y       | N       | N       | N       | N?      |
    | Josephus        | N       | N       | N       | N       | Y?      | N       | Y?      |
    | 12Patriarch     | N       | N       | N       | N?      | N       | N       | N       |
    | Psal 152-155    | N       | N       | N       | N       | Y?      | N       | N?      |
    | Ps of Sol       | N?      | N       | N       | N       | N?      | N       | N?      |
    | 2Baruch 1-77    | N       | N       | N       | N       | Y?      | N       | N?      |
    | 2Baruch 78-87   | N       | N       | N       | N       | Y?      | N       | Y?      |
    |                 |         |         |         |         |         |         |         |

[^0-43]: See Vreg Nersessian, *The Bible in the Armenian Tradition,* (Los 
    Angeles, The J. Paul Getty Musuem, 2001); Michael E. Stone, Armenian Canon Lists: The Council of Partaw [768 C.E.]", *Harvard Theological Review 66* (1973): pp. 479-486; Michael E. Stone, Armenian Canon Lists: the Stichometry of Anania of Shirak.", *Harvard Theological Review 68* (1975): pp. 253-260; Michael E. Stone, Armenian Canon Lists III: the Lists of Mechitar of Ayrivank [c. 1285 C.E.].", *Harvard Theological Review 69* (1976): pp. 289-300; Michael E. Stone, Armenian Canon Lists IV: The List of Gregory of Tat'ew [14th Century].", *Harvard Theological Review 72* (1980): pp. 237-294; Michael E. Stone, Armenian Canon Lists V: Anyonymous Texts." *Harvard Theological Review 83* (1990): pp. 141-161; The previous four articles can be purchased at https://www.cambridge.org/core/journals/harvard-theological-review/article/armenian-canon-lists-ivthe-list-of-gregory-of-tatew-14th-century/549FA7C411E0B0338C479589937027EC Michael E. Stone, *Selected Studies in Pseudepigrapha and Apocrypha With Special Reference to Armenian Tradition,* (New York: E. J. Brill, 1991); 

[^0-45]: The New Catholic Encylopedia says,
    
    > “St. Jerome distinguished between canonical books and ecclesiastical books. The latter he judged were circulated by the Church as good spiritual reading but were not recognized as authoritative Scripture. The situation remained unclear in the ensuing centuries…For example, John of Damascus, Gregory the Great, Walafrid, Nicolas of Lyra and Tostado continued to doubt the canonicity of the deuterocanonical books. According to Catholic doctrine, the proximate criterion of the biblical canon is the infallible decision of the Church. This decision was not given until rather late in the history of the Chruch at the Council of Trent. The Council of Trent definitively settled the matter of the Old Testament Canon. That this had not been done previously is apparent from the uncertainty that persisted up to the time of Trent (The New Catholic Encyclopedia, The Canon).

"""

assert_equal(find_enclosing_footnote_id(test_file, 26973), '0-18')
assert_equal(find_footnote_marker_position(test_file, '0-18'), 2261)

test_file2 = """{pagebreak}

Trent had to claim this authority to be able to add books to the canon at any time because the vast majority of the church fathers prior to Trent held to the Protestant canon. This of course contradicts their definitions of what constitutes the catholic faith. They say that catholic doctrine is whatever has the universal consent of the church. But that's the problem - none of Rome's distinctive doctrines has had the universal consent of the church - none of them. That is why all the Reformers (without exception) said that Protestantism is the catholic faith and that the Romanists had abandoned the catholic faith. They demonstrated that the church of the first twelve centuries was Protestant. And this was certainly the case when it came to what books should be in the canon. In fact, that was true all the way up to the Council of Trent. 

Jerome, the translator of their Latin Vulgate Bible, translated the apocrypha because it was useful background history (just like we treat it as useful history), but he denied that the apocrypha was inspired, inerrant, or part of the canon of Scripture. Later in this book I will show hundreds of the most influential church fathers held to the Protestant canon. Even the official Catholic Encyclopedia admits that the majority opinion in the church prior to Trent goes against the apocrypha,[^0-42] but they insist that the Council of Trent was still led by God to make an infallible decision to add the apocrypha to the canon. 

My response to that is to ask, "Why was Trent's vote to include the apocrypha an infallible vote when it was a minority vote?" The vote was 24 in favor, 15 opposed, and 16 uncertain and abstaining. So why were 24 of these church leaders infallibly guided in their "yes" vote while 31 of these church leaders were not infallibly guided in either their "no" vote or their abstentions? And furthermore, what makes their voted opinion more infallible than the opinion of the majority of the church fathers in previous centuries?[^0-43] What makes their voted opinion more official than the official marginal notes in the official Latin Vulgate Bible as late as 1498? We call these marginal notes the "Glossa Ordinaria." Though the Latin Vulgate Bible contained the apocrypha as useful background material (just like many Protestant Bibles did), it emphatically declared that the apocryphal books were not inspired Scripture. That was the official catholic Bible up through the time of Trent. When commenting on Apocryphal books, these marginal notes clearly distinguish them from canonical Scripture. At the beginning of the apocryphal book of Tobit it says, "Here begins the book of Tobit which is not in the canon," or "Here begins the book of Judith which is not in the canon," etc. The Prologue to the Glossa ordinaria (written in AD 1498) maintained a distinction between canonical and apocryphal books, stating that though both are included in the Bible, the canonical books are inspired and the apocryphal books are not.[^0-44] 

This represented the views of a huge number of the most influential and well-known scholars of the previous twelve centuries.  Even Cajetan, the most famous Romanist scholar at the time of the Reformation said that the Church of his day followed Jerome in believing the Bible only had 66 books. That was a huge admission that Trent's view is not the catholic view (small c catholic). Even the Cardinal Francisco Jiménez de Cisneros, the Archbishop of Toledo, and Grand Inquisitor against Protestants, did not believe the apocryphal books were inspired. Cinsneros in collaboration with the leading theologians of his day, produced an edition of the Bible called the Biblia Complutensia or the Complutensian Polyglot Bible. There is an admonition in the Preface that states that the books of Tobit, Judith, Wisdom, Ecclesiasticus, the Maccabees and the additions to Esther and Daniel are not canonical Scriptures and therfore could not be used to confirm any fundamental points of doctrine, though the church used them for reading and edification. No wonder it was a minority vote. This all looks more like changing church policy than an infallible decision.


[^0-44]: The Prologue to the Glossa ordinaria (1498 AD), states,
Many people, who do not give much attention to the holy scriptures, think that all the books contained in the Bible should be honored and adored with equal veneration, not knowing how to distinguish among the canonical and non-canonical books, the latter of which the Jews number among the apocrypha. Therefore they often appear ridiculous before the learned; and they are disturbed and scandalized when they hear that someone does not honor something read in the Bible with equal veneration as all the rest. Here, then, we distinguish and number distinctly first the canonical books and then the non-canonical, among which we further distinguish between the certain and the doubtful.

    The canonical books have been brought about through the dictation of the Holy Spirit. It is not known, however, at which time or by which authors the non-canonical or apocryphal books were produced. Since, nevertheless, they are very good and useful, and nothing is found in them which contradicts the canonical books, the church reads them and permits them to be read by the faithful for devotion and edification. Their authority, however, is not considered adequate for proving those things which come into doubt or contention, or for confirming the authority of ecclesiastical dogma, as blessed Jerome states in his prologue to Judith and to the books of Solomon. But the canonical books are of such authority that whatever is contained therein is held to be true firmly and indisputably, and likewise that which is clearly demonstrated from them. For just as in philosophy a truth is known through reduction to self-evident first principles, so too, in the writings handed down from holy teachers, the truth is known, as far as those things that must be held by faith, through reduction to the canonical scriptures that have been produced by divine revelation, which can contain nothing false. Hence, concerning them Augustine says to Jerome: To those writers alone who are called canonical I have learned to offer this reverence and honor: I hold most firmly that none of them has made an error in writing. Thus if I encounter something in them which seems contrary to the truth, I simply think that the manuscript is incorrect, or I wonder whether the translator has discovered what the word means, or whether I have understood it at all. But I read other writers in this way: however much they abound in sanctity or teaching, I do not consider what they say true because they have judged it so, but rather because they have been able to convince me from those canonical authors, or from probable arguments, that it agrees with the truth. Translation by Dr. Michael Woodward from the following latin:

    Quoniam plerique eo quod non multam operam dant sacrae Scripturae, existimant omnes libros qui in Bibliis continentur, pari veneratione esse reverendos atque adorandos, nescientes distinguere inter libros canonicos, et non canonicos, quos Hebraei a canone separant, et Graeci inter apocrypha computant; unde saepe coram doctis ridiculi videntur, et perturbantur, scandalizanturque cum audiunt aliquem non pari cum caeteris omnibus veneratione prosequi aliquid quod in Bibliis legatur: idcirco hic distinximus, et distincte numeravimus primo libros canonicos, et postea non canonicos, inter quos tantum distat quantum inter certum et dubium. Nam canonici sunt confecti Spiritus sancto dictante non canonici autem sive apocryphi, nescitur quo tempore quibusve auctoribus autoribus sint editi; quia tamen valde boni et utiles sunt, nihilque in eis quod canonicis obviet, invenitur, ideo Ecclesia eos legit, et permittit, ut ad devotionem, et ad morum informationem a fidelibus legantur. Eorum tamen auctoritas ad probandum ea quae veniunt in dubium, aut in contentionem, et ad confirmandam ecclesiasticorum dogmatum auctoritatem, non reputatur idonea, ut ait beatus Hieronymus in prologis super Judith et super libris Salomonis. At libri canonici tantae sunt auctoritatis, ut quidquid ibi continetur, verum teneat firmiter et indiscusse: et per consequens illud quod ex hoc concluditur manifeste; nam sicut in philosophia veritas cognoscitur per reductionem ad prima principia per se nota: ita et in Scripturis a sanctis doctoribus traditis veritas cognoscitur, quantum ad ea quae sunt fide tenenda, per reductionem ad Scripturas canonicas, quae sunt habita divina revelatione cui nullo modo potest falsum subesse. Unde de his dicit Augustinus ad Hieronymum: Ego solis eis scriptoribus qui canonici appellantur, didici hunc timorem honoremque deferre, ut nullum eorum scribendo errasse firmissime teneam; ac si aliquid in eis offendero quod videatur contrarium veritati, nihil aliud existimem quam mendosum esse codicem, vel non esse assecutum interpretem quod dictum est, vel me minime intellexisse, non ambigam. Alios autem ita lego, ut quantalibet sanctitate doctrinave polleant, non ideo verum putem quia ipsi ita senserunt, sed quia mihi per illos auctores canonicos vel probabiles rationes, quod a vero non abhorreat, persuadere potuerunt (Biblia cum glosa ordinaria et expositione Lyre litterali et morali (Basel: Petri & Froben, 1498), British Museum IB.37895, Vol. 1, On the canonical and non-canonical books of the Bible. Translation by Dr. Michael Woodward).


"""

assert_equal(find_enclosing_footnote_id(test_file2, 4193), '0-44')
assert_equal(find_footnote_marker_position(test_file2, '0-44'), 3023)
assert_equal(get_footnote_body_position(test_file2, '0-44'), 4193)


print('Passing!')
