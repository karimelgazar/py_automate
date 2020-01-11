import os
import webbrowser
from tkinter import filedialog, Tk
import os


#TODO ADD emoji to the buttons

#TODO ADD a shortcut to collapse the side bar (Alt+b)

#TODO ADD a button to move to the next lesson in the last concept

#TODO ADD a button to move to the previous lesson in the first concept

def decorate(html_file, files):
    """
    THIS METHOD: adds decoration to the html files 
    you sholud edit the variable [decoration]
    below to add a new decoration to the html 

    Arguments:
    =========
        html_file  -- the html file to edit
        files  -- all html files in this folder
    """

    decoration = '''

    <!-- MY NEW DECORATION  -->
    
      <div class = "row" >
        <div class = "col-12" >
            <p class="text-center" style="margin-top:50px;">
                XX1
            </p>
            <p class="text-center" style="margin-top:25px;">
                XX2
            </p>
            
        </div>
      </div>

    </div>
    <script src="../assets/js/jquery-3.3.1.min.js"></script>
    <script src="../assets/js/plyr.polyfilled.min.js"></script>
    <script src="../assets/js/bootstrap.min.js"></script>
    <script src="../assets/js/jquery.mCustomScrollbar.concat.min.js"></script>
    <script src="../assets/js/katex.min.js"></script>
 
     <script>

    // Initialize Plyr video players
    const players = Array.from(document.querySelectorAll('video')).map(p => new Plyr(p));

    // render math equations
    let elMath = document.getElementsByClassName('mathquill');
    for (let i = 0, len = elMath.length; i < len; i += 1) {
      const el = elMath[i];

      katex.render(el.textContent, el, {
        throwOnError: false
      });
    }

    // this hack will make sure Bootstrap tabs work when using Handlebars
    if ($('#question-tabs').length && $('#user-answer-tabs').length) {
      $("#question-tabs a.nav-link").on('click', function () {
        $("#question-tab-contents .tab-pane").hide();
        $($(this).attr("href")).show();
      });
      $("#user-answer-tabs a.nav-link").on('click', function () {
        $("#user-answer-tab-contents .tab-pane").hide();
        $($(this).attr("href")).show();
      });
    } else {
      $("a.nav-link").on('click', function () {
        $(".tab-pane").hide();
        $($(this).attr("href")).show();
      });
    }

    // side bar events
    $(document).ready(function () {
      $("#sidebar").mCustomScrollbar({
        theme: "minimal"
      });

      $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
      });

      // scroll to first video on page loading
      if ($('video').length) {
        $('html,body').animate({ scrollTop: $('div.plyr').prev().offset().top});
      }

      // auto play first video: this may not work with chrome/safari due to autoplay policy
      if (players && players.length > 0) {
        players[0].play();
      }

      // scroll sidebar to current concept
      XX3
      // currentInSideBar.css( "text-decoration", "highlight" );
      currentInSideBar.css( "background-color", "green" );
      $("#sidebar").mCustomScrollbar('scrollTo', currentInSideBar);
    });
    </script>
    </body>

    </html>
    '''
    previous_button = ''
    next_button = ''
    indx = files.index(html_file)

    # scrollbar = "\t\tconst currentInSideBar = $(\"ul.sidebar-list.components li a:contains(\'{}\')\")".format(
    #     html_file[:-5])

    # mCSB_1_container > ul.sidebar-list.list-unstyled.components > li:nth-child(32) > a
    scrollbar = "\t\tconst currentInSideBar = $(\"#mCSB_1_container > ul.sidebar-list.list-unstyled.components > li:nth-child({}) > a\")".format(
        indx + 1)

    if indx > 0:
        previous_button = "<a href=\"{}\" class=\"btn btn-warning\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;\">Previous Concept</a>".format(
            files[indx - 1])

    if indx < (len(files) - 1):
        next_button = "<a href=\"{}\" class=\"btn btn-success\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;\">Next Concept</a>".format(
            files[indx + 1])

    # if ascii errors occured when
    #  encoding to UTF-8 just ignore them
    old = open(html_file, "r", encoding="UTF-8", errors='ignore').readlines()

    with open(html_file, "w", encoding="UTF-8", errors='ignore') as new:
        for line in old:

            # this is so important you should use
            # </main> so that you can add new features freely
            # and not to affect the page original source code
            if '</main>' in line:
                new.write(line)  # write this line

                # add the decoration
                new_decoration = decoration.replace('XX1', next_button)
                new_decoration = new_decoration.replace('XX2', previous_button)

                new.write(new_decoration.replace('XX3', scrollbar))
                print("Done With File: {}".format(html_file))
                return
            else:
                new.write(line)


def extract_html_in(dirctory):
    if 'Part' in dirctory:
        print(dirctory)
        print('=' * 30)

        os.chdir(dirctory)

        htmls = sorted([x for x in os.listdir(dirctory) if x.endswith(
            '.html') and not x.startswith('index')])
        for html in htmls:
            decorate(html, htmls)
        print('this folder is finished\n'.title())


def pick_course():
  # Pick HTMLs Folder
    Tk().withdraw()  # to hide the small tk window
    path = filedialog.askdirectory()  # folder picker

    for item in os.listdir(path):
        # ? the whole course was given
        item_absolute_path = os.path.join(path, item)
        if os.path.isdir(item_absolute_path):
            extract_html_in(item_absolute_path)

        # ? a folder for a single module was given not the whole course
        else:
            extract_html_in(path)


pick_course()
