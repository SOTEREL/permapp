serve:
	bundle exec jekyll serve --livereload

install:
	gem install jekyll bundler
	bundle install
	bundle update
